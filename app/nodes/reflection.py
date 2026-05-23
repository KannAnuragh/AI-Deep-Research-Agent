from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=GEMINI_API_KEY
)

def _response_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):
                parts.append(item.get("text", ""))

            elif hasattr(item, "text"):
                parts.append(item.text)

            else:
                parts.append(str(item))

        return "\n".join(parts)

    return str(content)

def reflection_node(state):

    summaries = state["summaries"]

    joined = "\n\n".join(
        str(s) for s in summaries
    )

    prompt = f"""
    You are evaluating research quality.

    SUMMARY:
    {joined}

    Evaluate the following:

    1. Are there enough factual sources?
    2. Are multiple perspectives covered?
    3. Are important counterarguments missing?
    4. Is technical depth sufficient?
    5. Are there unsupported claims?
    6. Are important topics unexplored?

    If the research is sufficient:
    RESEARCH_COMPLETE: YES

    Otherwise:
    RESEARCH_COMPLETE: NO

    Then explain:
    - what is missing
    - what should be researched next
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    reflection = _response_text(response.content)

    complete = "RESEARCH_COMPLETE: YES" in reflection

    return {
        "reflection": reflection,
        "research_complete": complete
    }
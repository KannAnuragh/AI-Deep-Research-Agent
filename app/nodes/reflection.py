from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from app.config import GEMINI_API_KEY

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
You are a research evaluator.

Analyze the current research summary.

SUMMARY:
{joined}

Evaluate:
- completeness
- technical depth
- missing perspectives
- missing evidence
- weak areas

Decide whether more research is needed.

Return format:

RESEARCH_COMPLETE: YES or NO

REASON:
...
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
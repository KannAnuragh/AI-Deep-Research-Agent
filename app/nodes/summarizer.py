from config import GEMINI_API_KEY  # noqa: F401
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")


def _response_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    return str(content)

def summarize_results(query, results):

    content += f"""

    ========================
    SOURCE
    ========================

    TITLE:
    {r.get('title')}

    URL:
    {r.get('url')}

    CONTENT:
    {r.get('content')}

    """

    prompt = f"""
    You are a research analyst.

    Research Question:
    {query}

    Analyze and summarize.

    For every major claim:
    - mention the source title
    - preserve important URLs

    Focus on:
    - key findings
    - statistics
    - trends
    - insights

    Information:
    {content}
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return _response_text(response.content)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=GEMINI_API_KEY
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

def summarize_node(state):

    results = state["search_results"]

    content = ""

    for r in results:

        content += f"""

========================
SOURCE
========================

TITLE:
{r.get("title")}

URL:
{r.get("url")}

CONTENT:
{r.get("content")}

"""

    prompt = f"""
    Analyze and summarize the following research findings.

    RESEARCH DATA:
    {content}

    Focus on:
    - important insights
    - trends
    - major claims
    - psychological theories
    - neuroscience aspects
    - evolutionary explanations

    Rules:
    - only use provided research data
    - do not invent claims
    - preserve technical accuracy
    - synthesize overlapping findings

    Write a concise but detailed research summary.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    summary_text = _response_text(response.content)

    existing = state.get("summaries", [])

    return {
        "summaries": existing + [summary_text]
    }
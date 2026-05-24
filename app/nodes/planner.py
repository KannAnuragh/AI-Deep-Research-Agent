import re

from langchain_core.messages import HumanMessage

from app.llm import research_llm

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

def planner_node(state):

    user_query = state["user_query"]

    prompt = f"""
Generate exactly 5 web search queries.

TOPIC:
{user_query}

RULES:
- Return ONLY search queries
- One query per line
- No explanations
- No markdown
- No numbering
- No headings
- No bullet points
- No descriptions
"""

    response = research_llm.invoke([
        HumanMessage(content=prompt)
    ])

    text = _response_text(response.content)

    queries = text.splitlines()

    cleaned = []

    for q in queries:

        q = re.sub(r"^\d+\.\s*", "", q)
        q = q.replace('"', "").strip()

        if len(q) > 10:
            cleaned.append(q)

    return {
        "search_queries": cleaned[:5]
    }
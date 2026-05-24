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

def query_refinement_node(state):

    reflection = state["reflection"]

    previous_queries = state["search_queries"]

    joined_queries = "\n".join(previous_queries)

    prompt = f"""
You are a research strategist.

The current research process identified missing areas.

REFLECTION:
{reflection}

PREVIOUS SEARCH QUERIES:
{joined_queries}

Generate 5 NEW search queries that:
- explore missing perspectives
- avoid repeating previous searches
- deepen technical coverage
- investigate unexplored aspects

RULES:
- return ONLY queries
- one query per line
- no numbering
- no markdown
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
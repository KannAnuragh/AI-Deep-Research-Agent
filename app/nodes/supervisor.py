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

def supervisor_node(state):

    query = state["user_query"]

    prompt = f"""
You are a research supervisor.

Break the topic into exactly 4 major technical research sections.

TOPIC:
{query}

RULES:
- Return ONLY sections
- One section per line
- No descriptions
- No numbering
- No markdown
- No explanations
"""

    response = research_llm.invoke([
        HumanMessage(content=prompt)
    ])

    text = _response_text(response.content)

    raw_sections = text.splitlines()

    sections = []

    for s in raw_sections:

        s = re.sub(r"^\d+\.\s*", "", s)
        s = s.replace("-", "").strip()

        if len(s) > 5:

            sections.append({
                "name": s,
                "description": s
            })

    # FALLBACK SAFETY
    if not sections:

        sections = [
            {
                "name": query,
                "description": query
            }
        ]

    print("\nSUPERVISOR SECTIONS:\n")

    for s in sections:
        print("-", s["name"])

    return {
        "sections": sections
    }
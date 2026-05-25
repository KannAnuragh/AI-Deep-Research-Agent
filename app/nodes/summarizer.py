from langchain_core.messages import HumanMessage

from app.llm import research_llm
from app.prompts import SUMMARIZER_PROMPT


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
    section = state["current_section"]

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

    prompt = SUMMARIZER_PROMPT.format(
        section=section,
        content=content
    )

    response = research_llm.invoke([
        HumanMessage(content=prompt)
    ])

    summary_text = _response_text(response.content)

    existing = state.get("summaries", {})
    existing[section] = summary_text

    print(f"\nSUMMARIZED SECTION: {section}\n")

    return {
        "summaries": existing
    }
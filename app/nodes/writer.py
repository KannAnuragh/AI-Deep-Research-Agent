from langchain_core.messages import HumanMessage

from app.llm import research_llm
from app.prompts import WRITER_PROMPT


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


def writer_node(state):

    summaries = state["summaries"]

    joined = ""

    for section, summary in summaries.items():
        joined += f"""
# SECTION: {section}

{summary}

"""

    prompt = WRITER_PROMPT.format(joined=joined)

    response = research_llm.invoke([
        HumanMessage(content=prompt)
    ])

    print("\nWRITER: FINAL REPORT GENERATED\n")

    return {
        "final_report": _response_text(response.content)
    }
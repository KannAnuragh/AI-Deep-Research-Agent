from langchain_core.messages import HumanMessage

from app.llm import research_llm

def writer_node(state):

    summaries = state["summaries"]

    joined = ""

    for section, summary in summaries.items():

        joined += f"""

    # SECTION
    {section}

    {summary}

    """

    prompt = f"""
Write a clean markdown research report.

Findings:
{joined}

IMPORTANT RULES:
- do not invent facts
- do not fabricate statistics
- do not invent dates
- do not add fictional stakeholders
- do not use memo formatting
- avoid unsupported claims
- preserve technical accuracy

ONLY use these sections:

# Title

# Executive Summary

# Main Findings

# Trends

# Risks

# Conclusion
"""

    response = research_llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "final_report": _response_text(response.content)
    }

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
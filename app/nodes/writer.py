from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=GEMINI_API_KEY
)

def writer_node(state):

    summaries = state["summaries"]

    joined = "\n\n".join(
        str(s) for s in summaries
    )
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

    response = llm.invoke([
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
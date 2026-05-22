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

def generate_report(user_query, summaries):

    joined = "\n\n".join(summaries)

    prompt = f"""
    Write a professional research report.

    Research Topic:
    {user_query}

    Findings:
    {joined}

    IMPORTANT RULES:
    - Do not invent statistics
    - Do not fabricate predictions
    - Only use information from findings
    - Clearly state uncertainty
    - Avoid unsupported claims

    Structure:
    - Executive Summary
    - Main Findings
    - Key Trends
    - Risks
    - Conclusion

    Use markdown formatting.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return _response_text(response.content)
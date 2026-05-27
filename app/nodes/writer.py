from langchain_core.messages import HumanMessage

from app.llm import research_llm
from app.prompts import SYNTHESIS_PROMPT, EXECUTIVE_SUMMARY_PROMPT


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
    user_query = state.get("user_query", "")

    # Build joined section summaries
    joined = ""
    for section, summary in summaries.items():
        joined += f"\n# SECTION: {section}\n\n{summary}\n\n"

    # =========================================
    # PASS 1 — Dense technical body
    # Write Main Findings, Trends, Risks, Conclusion
    # NO executive summary yet
    # =========================================

    print("\nWRITER PASS 1: synthesising technical body...\n")

    body_response = research_llm.invoke([
        HumanMessage(
            content=SYNTHESIS_PROMPT.format(
                query=user_query,
                joined=joined
            )
        )
    ])

    body = _response_text(body_response.content)

    # =========================================
    # PASS 2 — Executive summary
    # Derived LAST from the dense body content
    # =========================================

    print("\nWRITER PASS 2: deriving executive summary...\n")

    exec_response = research_llm.invoke([
        HumanMessage(
            content=EXECUTIVE_SUMMARY_PROMPT.format(
                query=user_query,
                body=body
            )
        )
    ])

    exec_summary = _response_text(exec_response.content)

    # =========================================
    # ASSEMBLE — Title → Exec Summary → Body
    # =========================================

    title = f"# {user_query.title()}\n"

    final_report = (
        title
        + "\n"
        + exec_summary.strip()
        + "\n\n"
        + body.strip()
    )

    print("\nWRITER: FINAL REPORT GENERATED\n")

    return {
        "final_report": final_report
    }
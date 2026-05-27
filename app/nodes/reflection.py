from app.llm import research_llm
from app.schemas import ReflectionOutput
from app.prompts import REFLECTION_PROMPT

# Minimum quantitative score to pass reflection
QUANTITATIVE_THRESHOLD = 3


def reflection_node(state):

    section = state["current_section"]
    sections = state.get("sections", [])
    summaries = state.get("summaries", {})
    adversarial_feedback = state.get("adversarial_feedback", "")

    # Find section description
    description = ""
    for s in sections:
        if s["name"] == section:
            description = s.get("description", "")
            break

    current_summary = summaries.get(section, "")

    prompt = REFLECTION_PROMPT.format(
        section=section,
        description=description,
        summary=current_summary,
        adversarial_feedback=adversarial_feedback
    )

    response = research_llm.invoke_structured(
        ReflectionOutput,
        prompt
    )

    print(f"\nREFLECTION FOR: {section}")
    print(f"  LLM COMPLETE:       {response.research_complete}")
    print(f"  QUANTITATIVE SCORE: {response.quantitative_score}/5")
    print(f"  SUFFICIENT DEPTH:   {response.has_sufficient_depth}")
    print(f"  REASONING: {response.reasoning}\n")

    # Priority 1 — hard gate: insufficient quantitative evidence → force re-research
    if response.quantitative_score < QUANTITATIVE_THRESHOLD:
        print(
            f"  GATE FAILED: quantitative_score "
            f"{response.quantitative_score} < {QUANTITATIVE_THRESHOLD} "
            f"— forcing re-research\n"
        )
        research_complete = False

    # Priority 2 — hard gate: missing technical depth subcategories
    elif not response.has_sufficient_depth:
        print(
            "  GATE FAILED: technical depth subcategories incomplete "
            "— forcing re-research\n"
        )
        research_complete = False

    else:
        research_complete = response.research_complete

    return {
        "reflection": response.reasoning,
        "missing_topics": response.missing_topics,
        "research_complete": research_complete,
    }
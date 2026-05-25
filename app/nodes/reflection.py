from app.llm import research_llm
from app.schemas import ReflectionOutput
from app.prompts import REFLECTION_PROMPT


def reflection_node(state):

    section = state["current_section"]
    sections = state.get("sections", [])
    summaries = state.get("summaries", {})

    # Get description for current section
    description = ""
    for s in sections:
        if s["name"] == section:
            description = s.get("description", "")
            break

    # Only evaluate the current section's summary
    current_summary = summaries.get(section, "")

    prompt = REFLECTION_PROMPT.format(
        section=section,
        description=description,
        summary=current_summary
    )

    response = research_llm.invoke_structured(
        ReflectionOutput,
        prompt
    )

    print(f"\nREFLECTION FOR: {section}")
    print(f"COMPLETE: {response.research_complete}")
    print(f"REASONING: {response.reasoning}\n")

    return {
        "reflection": response.reasoning,
        "research_complete": response.research_complete
    }
from app.llm import research_llm
from app.schemas import PlannerOutput
from app.prompts import PLANNER_PROMPT


def planner_node(state):

    user_query = state["user_query"]
    current_section = state.get("current_section", "")
    sections = state.get("sections", [])

    # Find description for the current section
    description = ""
    for s in sections:
        if s["name"] == current_section:
            description = s.get("description", "")
            break

    prompt = PLANNER_PROMPT.format(
        query=user_query,
        section=current_section,
        description=description
    )

    response = research_llm.invoke_structured(
        PlannerOutput,
        prompt
    )

    print(f"\nPLANNER QUERIES FOR: {current_section}\n")
    for q in response.queries:
        print("-", q)

    return {
        "search_queries": response.queries
    }
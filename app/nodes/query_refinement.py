from app.llm import research_llm
from app.schemas import QueryRefinementOutput
from app.prompts import QUERY_REFINEMENT_PROMPT


def query_refinement_node(state):

    reflection = state["reflection"]
    section = state.get("current_section", "")

    prompt = QUERY_REFINEMENT_PROMPT.format(
        section=section,
        reflection=reflection
    )

    response = research_llm.invoke_structured(
        QueryRefinementOutput,
        prompt
    )

    print(f"\nREFINED QUERIES FOR: {section}\n")
    for q in response.refined_queries:
        print("-", q)

    return {
        "search_queries": response.refined_queries
    }
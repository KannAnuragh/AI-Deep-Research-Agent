from app.llm import research_llm
from app.schemas import QueryRefinementOutput
from app.prompts import QUERY_REFINEMENT_PROMPT


def query_refinement_node(state):

    reflection = state.get("reflection", "")
    missing_topics = state.get("missing_topics", [])
    adversarial_feedback = state.get("adversarial_feedback", "")
    section = state.get("current_section", "")

    # Format structured gap list for the prompt
    topics_str = (
        "\n".join(f"- {t}" for t in missing_topics)
        if missing_topics
        else "See reflection reasoning below."
    )

    prompt = QUERY_REFINEMENT_PROMPT.format(
        section=section,
        reflection=reflection,
        missing_topics=topics_str,
        adversarial_feedback=adversarial_feedback
    )

    response = research_llm.invoke_structured(
        QueryRefinementOutput,
        prompt
    )

    print(f"\nREFINED QUERIES FOR: {section}\n")
    for q in response.refined_queries:
        print(f"  - {q}")

    return {
        "search_queries": response.refined_queries
    }
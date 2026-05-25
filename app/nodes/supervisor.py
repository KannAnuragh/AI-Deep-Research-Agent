from app.llm import research_llm
from app.schemas import SupervisorOutput
from app.prompts import SUPERVISOR_PROMPT


def supervisor_node(state):

    query = state["user_query"]

    prompt = SUPERVISOR_PROMPT.format(query=query)

    response = research_llm.invoke_structured(
        SupervisorOutput,
        prompt
    )

    sections = [
        {
            "name": section.name,
            "description": section.description
        }
        for section in response.sections
    ]

    print("\nSUPERVISOR SECTIONS:\n")

    for s in sections:
        print("-", s["name"])

    return {
        "sections": sections
    }
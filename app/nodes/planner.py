import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview"
)

def planner_node(state):

    user_query = state["user_query"]

    prompt = f"""
    You are a research planner.

    Generate 5 high-quality search queries.

    Topic:
    {user_query}

    Cover:
    - fundamentals
    - applications
    - trends
    - comparisons
    - modern developments
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    queries = response.content.splitlines()

    cleaned = [
        re.sub(r"^\d+\.\s*", "", q)
        .strip()
        for q in queries
        if q.strip()
    ]

    return {
        "search_queries": cleaned
    }
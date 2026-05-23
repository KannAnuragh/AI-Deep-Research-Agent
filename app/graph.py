from langgraph.graph import StateGraph, START, END

from state import ResearchState

from nodes.planner import planner_node
from nodes.search import search_node
from nodes.summarizer import summarize_node
from nodes.reflection import reflection_node
from nodes.writer import writer_node

builder = StateGraph(ResearchState)

builder.add_node("planner", planner_node)
builder.add_node("search", search_node)
builder.add_node("summarize", summarize_node)
builder.add_node("reflection", reflection_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "reflection")

def should_continue(state):

    if state["research_complete"]:
        return "writer"

    if state["iteration_count"] >= 3:
        return "writer"

    return "search"

builder.add_conditional_edges(
    "reflection",
    should_continue
)

builder.add_edge("writer", END)

graph = builder.compile()
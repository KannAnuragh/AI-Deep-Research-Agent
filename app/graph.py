from langgraph.graph import StateGraph, START, END

from app.state import ResearchState

from app.nodes.supervisor import supervisor_node
from app.nodes.section_selector import section_selector_node
from app.nodes.worker import worker_node
from app.nodes.summarizer import summarize_node
from app.nodes.writer import writer_node

builder = StateGraph(ResearchState)

# Nodes
builder.add_node("supervisor", supervisor_node)
builder.add_node("section_selector", section_selector_node)
builder.add_node("worker", worker_node)
builder.add_node("summarize", summarize_node)
builder.add_node("writer", writer_node)

# Flow
builder.add_edge(START, "supervisor")

builder.add_edge(
    "supervisor",
    "section_selector"
)

builder.add_edge(
    "section_selector",
    "worker"
)

builder.add_edge(
    "worker",
    "summarize"
)

def should_continue(state):

    sections = state["sections"]

    summaries = state.get("summaries", {})

    # All sections completed
    if len(summaries) >= len(sections):
        return "writer"

    return "section_selector"

builder.add_conditional_edges(
    "summarize",
    should_continue
)

builder.add_edge("writer", END)

graph = builder.compile()
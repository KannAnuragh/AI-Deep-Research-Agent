from langgraph.graph import StateGraph, START, END

from app.state import ResearchState

from app.nodes.supervisor import supervisor_node
from app.nodes.section_selector import section_selector_node
from app.nodes.planner import planner_node
from app.nodes.worker import worker_node
from app.nodes.summarizer import summarize_node
from app.nodes.reflection import reflection_node
from app.nodes.query_refinement import query_refinement_node
from app.nodes.writer import writer_node

builder = StateGraph(ResearchState)

# =========================
# NODES
# =========================

builder.add_node("supervisor", supervisor_node)
builder.add_node("section_selector", section_selector_node)
builder.add_node("planner", planner_node)
builder.add_node("worker", worker_node)
builder.add_node("summarize", summarize_node)
builder.add_node("reflection", reflection_node)
builder.add_node("query_refinement", query_refinement_node)
builder.add_node("writer", writer_node)

# =========================
# MAIN FLOW
# =========================

builder.add_edge(START, "supervisor")
builder.add_edge("supervisor", "section_selector")
builder.add_edge("section_selector", "planner")   # planner now in the loop
builder.add_edge("planner", "worker")
builder.add_edge("worker", "summarize")
builder.add_edge("summarize", "reflection")

# =========================
# CONDITIONAL ROUTING
# =========================

def should_continue(state):

    iteration_count = state.get("iteration_count", 0)
    sections = state.get("sections", [])
    summaries = state.get("summaries", {})

    print(f"\nITERATION: {iteration_count}")

    # HARD STOP — write whatever we have
    if iteration_count >= 3:
        print("\nMAX ITERATIONS REACHED\n")
        return "writer"

    if state.get("research_complete", False):

        # Current section is done — check if more sections remain
        unsummarised = [
            s for s in sections
            if s["name"] not in summaries
        ]

        if unsummarised:
            print(
                f"\nSECTION COMPLETE — "
                f"{len(unsummarised)} section(s) remaining\n"
            )
            return "section_selector"

        print("\nALL SECTIONS COMPLETE — WRITING REPORT\n")
        return "writer"

    print("\nREFINING RESEARCH FOR CURRENT SECTION\n")
    return "query_refinement"

builder.add_conditional_edges(
    "reflection",
    should_continue
)

# =========================
# RECURSIVE RESEARCH LOOP
# =========================

builder.add_edge("query_refinement", "worker")

# =========================
# FINAL OUTPUT
# =========================

builder.add_edge("writer", END)

graph = builder.compile()
from langgraph.graph import END, START, StateGraph

from state import ResearchState

from nodes.planner import planner_node
from nodes.search import search_node
from nodes.summarizer import summarize_node
from nodes.writer import writer_node

builder = StateGraph(ResearchState)

# Add nodes
builder.add_node("planner", planner_node)
builder.add_node("search", search_node)
builder.add_node("summarize", summarize_node)
builder.add_node("writer", writer_node)

# Connect nodes
builder.add_edge(START, "planner")
builder.add_edge("planner", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "writer")
builder.add_edge("writer", END)

graph = builder.compile()
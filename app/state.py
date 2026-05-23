from typing import TypedDict, List

class SearchResult(TypedDict):
    title: str
    content: str
    url: str

class ResearchState(TypedDict):

    user_query: str

    search_queries: List[str]

    search_results: List[SearchResult]

    summaries: List[str]

    reflection: str

    research_complete: bool

    iteration_count: int

    final_report: str
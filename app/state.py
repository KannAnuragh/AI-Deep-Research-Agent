from typing import TypedDict, List, Dict

class SearchResult(TypedDict):
    title: str
    content: str
    url: str

class Section(TypedDict):
    name: str
    description: str

class ResearchState(TypedDict):

    user_query: str

    sections: List[Section]

    current_section: str

    search_queries: List[str]

    search_results: List[SearchResult]

    summaries: Dict[str, str]

    reflection: str

    research_complete: bool

    iteration_count: int

    final_report: str
from typing import TypedDict, List, Dict


class SearchResult(TypedDict):
    title: str
    content: str
    url: str
    credibility_score: float  # 0.0–1.0 from credibility.py


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

    # Adversarial review output for current section
    adversarial_feedback: str

    # Structured gap list from reflection (feeds query refinement)
    missing_topics: List[str]

    reflection: str

    research_complete: bool

    iteration_count: int

    final_report: str
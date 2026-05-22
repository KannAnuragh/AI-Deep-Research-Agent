from typing import TypedDict, List

class ResearchState(TypedDict):

    user_query: str

    search_queries: List[str]

    search_results: List[dict]

    summaries: List[str]

    final_report: str
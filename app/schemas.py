from pydantic import BaseModel
from typing import List

class Section(BaseModel):

    name: str

    description: str


class SupervisorOutput(BaseModel):

    sections: List[Section]


class PlannerOutput(BaseModel):

    queries: List[str]


class ReflectionOutput(BaseModel):

    research_complete: bool

    missing_topics: List[str]

    reasoning: str


class QueryRefinementOutput(BaseModel):

    refined_queries: List[str]
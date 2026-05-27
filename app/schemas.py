from pydantic import BaseModel, Field
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

    # Priority 1 — quantitative enforcement
    # Count of present items from:
    # equations, benchmark metrics, comparison data,
    # implementation constraints, performance claims
    # 0 = none found, 5 = all present
    quantitative_score: int = Field(
        ge=0, le=5,
        description="Count of quantitative evidence types present (0–5)"
    )

    # Priority 2 — depth enforcement
    # True only if all 6 subcategories are addressed:
    # architecture, tradeoffs, limitations,
    # performance, implementation complexity, resource cost
    has_sufficient_depth: bool


class QueryRefinementOutput(BaseModel):
    refined_queries: List[str]


class AdversarialOutput(BaseModel):

    # Priority 4 — adversarial agents

    skeptic_findings: List[str]
    # Weak or unsupported claims in the summary

    gaps_identified: List[str]
    # Missing technical dimensions or topics

    contradictions_found: List[str]
    # Conflicting claims between sources

    unverified_benchmarks: List[str]
    # Metrics cited without corroborating source

    overall_confidence: float = Field(
        ge=0.0, le=1.0,
        description="0.0 = no confidence, 1.0 = full confidence"
    )

    requires_more_research: bool
    # True if gaps or contradictions are severe enough to re-research
SUPERVISOR_PROMPT = """
Break this research topic into exactly 3 specific technical sections.

TOPIC:
{query}

RULES:
- Each section must be a distinct technical dimension (e.g. hardware architecture, control algorithms, performance analysis)
- Section names must be concise noun phrases, NOT "Introduction to..." or "Testing of..."
- Bad examples: "Introduction to X", "Overview of Y", "Testing and Validation of Z"
- Good examples: "FPGA Hardware Architecture and Resource Utilization", "PWM Modulation Algorithms and THD Optimization", "Gate Drive and Power Stage Design"
- Each section must be independently researchable
"""

PLANNER_PROMPT = """
Generate 5 high-quality technical search queries for the given section.

TOPIC:
{query}

SECTION:
{section}

SECTION DESCRIPTION:
{description}

The queries must be specific to this section, not the overall topic.
"""

SUMMARIZER_PROMPT = """
Analyze and summarize the following research findings for the section below.
For every important claim, mention the supporting source URL.

SECTION:
{section}

RESEARCH DATA:
{content}

Focus on:
- key facts and data points
- important insights and trends
- major claims and evidence
- technical details relevant to the section

Rules:
- only use provided research data
- do not invent claims
- preserve technical accuracy
- synthesize overlapping findings

Write a concise but detailed research summary.
"""

REFLECTION_PROMPT = """
Evaluate whether the current research for the section below is sufficient
for generating a high-quality technical report section.

SECTION:
{section}

SECTION DESCRIPTION:
{description}

CURRENT SUMMARY:
{summary}

IMPORTANT:
Research does NOT need to be perfect.

Mark research_complete as TRUE if:
- major technical concepts for this section are covered
- sufficient evidence exists
- the section can be reasonably written

Mark FALSE only if:
- critical information specific to this section is missing
- research is extremely shallow
- the section cannot be written from this data
"""

QUERY_REFINEMENT_PROMPT = """
Generate 5 new targeted search queries to fill the gaps identified in the reflection below.

SECTION:
{section}

REFLECTION:
{reflection}

The queries must directly address the missing topics identified.
"""

WRITER_PROMPT = """
Write a clean, well-structured markdown research report using the section summaries below.

SECTIONS AND FINDINGS:
{joined}

IMPORTANT RULES:
- do not invent facts
- do not fabricate statistics
- do not invent dates
- do not add fictional stakeholders
- do not use memo formatting
- avoid unsupported claims
- preserve technical accuracy

ONLY use these sections in this order:

# Title

# Executive Summary

# Main Findings

# Trends

# Risks

# Conclusion
"""
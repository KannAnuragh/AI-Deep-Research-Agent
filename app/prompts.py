# =============================================================
# SUPERVISOR
# =============================================================

SUPERVISOR_PROMPT = """
Break this research topic into exactly 3 specific technical sections.

TOPIC:
{query}

RULES:
- Each section must be a distinct technical dimension
- Section names must be concise noun phrases
- BAD: "Introduction to X", "Overview of Y", "Testing and Validation of Z"
- GOOD: "FPGA Hardware Architecture and Resource Utilization",
        "PWM Modulation Algorithms and THD Optimization",
        "Gate Drive Circuit Design and Power Stage Constraints"
- Each section must be independently researchable
- Each section must have a description explaining what technical
  sub-topics it should cover
"""

# =============================================================
# PLANNER
# =============================================================

PLANNER_PROMPT = """
Generate exactly 5 targeted technical search queries for the section below.

RESEARCH TOPIC:
{query}

SECTION:
{section}

SECTION DESCRIPTION:
{description}

REQUIREMENTS:
- Queries must target measurable, quantitative information:
  equations, benchmark figures, circuit parameters,
  comparison tables, efficiency numbers, resource counts
- Queries must be specific to this section, not the general topic
- Prefer queries likely to return IEEE papers, theses, or technical docs
"""

# =============================================================
# SUMMARIZER  (Priority 1 + 2)
# =============================================================

SUMMARIZER_PROMPT = """
You are a technical researcher. Analyse the sources below and produce a
structured technical summary for the section.

NOTE: Each source is labelled with a credibility tier and score.
Prioritise TIER-1 and TIER-2 sources. Treat TIER-5 sources as
supplementary only. Never cite a claim backed only by TIER-5 sources.

SECTION:
{section}

SOURCES:
{content}

OUTPUT STRUCTURE — you MUST include ALL six subsections:

## Architecture
Describe the hardware or algorithmic structure. Include block diagrams
described in text, component counts, or topology names.

## Tradeoffs
Compare at least two competing approaches. What does each sacrifice?
Cite sources for each position.

## Limitations
What constraints, failure modes, or boundary conditions apply?
State specific limits (e.g. maximum frequency, minimum deadtime).

## Performance Metrics  [REQUIRED — this section must contain numbers]
Include at minimum THREE of the following, with source citations:
- Equations or transfer functions
- Benchmark figures (THD%, efficiency%, frequency in Hz/kHz)
- Comparison table data (e.g. SPWM vs SVPWM THD at M=0.8)
- Implementation constraints (clock frequency, bit depth, LUT count)
- Measured performance claims (e.g. "3.91% THD at 21-level output")

If no quantitative data was found in the sources, write:
QUANTITATIVE DATA: NONE FOUND — explain what was searched.

## Implementation Complexity
Estimate development effort, HDL line count, toolchain requirements,
or design iterations needed. Reference any reported development time.

## Resource Cost
Report FPGA resource utilisation (LUTs, DSP blocks, BRAMs, FFs),
power consumption, BOM cost, or silicon area where available.

RULES:
- Only use data from provided sources
- Never invent statistics or equations
- Every numeric claim must reference its source URL
- Synthesise overlapping findings rather than listing them separately
"""

# =============================================================
# ADVERSARIAL REVIEW  (Priority 4)
# =============================================================

ADVERSARIAL_PROMPT = """
You are a rigorous technical peer reviewer. Your job is to challenge
the research summary below, not validate it.

SECTION:
{section}

SECTION DESCRIPTION:
{description}

SOURCE MANIFEST (with credibility scores):
{sources}

RESEARCH SUMMARY TO CHALLENGE:
{summary}

YOUR TASK — act as four agents simultaneously:

SKEPTIC AGENT:
- List every claim that lacks a specific numeric citation
- Flag vague language: "improves performance", "reduces harmonics", "efficient"
- These must become entries in skeptic_findings

GAP FINDER:
- Which of these six subcategories are missing or shallow?
  architecture / tradeoffs / limitations /
  performance metrics / implementation complexity / resource cost
- What specific topics are absent that the section description requires?
- These must become entries in gaps_identified

CONTRADICTION DETECTOR:
- Do any sources disagree on numbers, techniques, or conclusions?
- Are there conflicting efficiency claims, THD values, or frequency limits?
- These must become entries in contradictions_found

BENCHMARK VERIFIER:
- List every numeric benchmark cited in the summary
- For each, note whether at least two independent sources corroborate it
- Uncorroborated benchmarks → entries in unverified_benchmarks

SCORING:
- overall_confidence: your estimate of summary reliability (0.0–1.0)
  0.0 = mostly unsupported claims
  1.0 = all claims quantitatively corroborated by TIER-1/2 sources
- requires_more_research: true if gaps or contradictions are severe
  enough that the section CANNOT be written to technical standard
"""

# =============================================================
# REFLECTION  (Priority 1 + 2 gates)
# =============================================================

REFLECTION_PROMPT = """
Evaluate the research quality for the section below.
You also have adversarial review findings to consider.

SECTION:
{section}

SECTION DESCRIPTION:
{description}

CURRENT SUMMARY:
{summary}

ADVERSARIAL REVIEW FINDINGS:
{adversarial_feedback}

EVALUATE THE FOLLOWING:

1. research_complete
   Mark TRUE only if:
   - All six subcategories are addressed (architecture, tradeoffs,
     limitations, performance, implementation complexity, resource cost)
   - Quantitative evidence is present (equations, benchmarks, comparisons,
     constraints, or measured performance claims)
   - Adversarial review found no severe gaps or contradictions

   Mark FALSE if any of the above conditions are not met.

2. missing_topics
   List the specific topics that are missing or inadequately covered.
   Be precise: "switching frequency benchmark" not "more detail needed".

3. reasoning
   One paragraph explaining your decision.

4. quantitative_score (0–5)
   Count how many of these are present in the summary:
   - [ ] Mathematical equations or transfer functions
   - [ ] Benchmark figures with units (THD%, Hz, efficiency%)
   - [ ] Comparison table data between two or more techniques
   - [ ] Implementation constraints (clock speed, bit depth, LUT count)
   - [ ] Measured performance claims with source citation
   Score = number of boxes checked (0 to 5).

5. has_sufficient_depth (true/false)
   True only if ALL six subcategories are non-trivially addressed.
"""

# =============================================================
# QUERY REFINEMENT  (now uses structured missing_topics)
# =============================================================

QUERY_REFINEMENT_PROMPT = """
Generate exactly 5 new search queries to fill the research gaps below.

SECTION:
{section}

STRUCTURED MISSING TOPICS (from reflection):
{missing_topics}

REFLECTION REASONING:
{reflection}

ADVERSARIAL FINDINGS:
{adversarial_feedback}

REQUIREMENTS:
- Each query must target one specific missing topic
- Queries must seek quantitative data: equations, benchmarks,
  measured results, comparison tables, implementation figures
- Prefer queries that will return IEEE papers, technical reports,
  or manufacturer datasheets
- Do NOT repeat queries that were already used
"""

# =============================================================
# WRITER PASS 1 — Dense technical synthesis  (Priority 5)
# Executive summary is NOT written here
# =============================================================

SYNTHESIS_PROMPT = """
Write a dense, technically rigorous research report body.
Do NOT write an executive summary — that comes separately.

RESEARCH TOPIC:
{query}

SECTION SUMMARIES:
{joined}

OUTPUT — write ONLY these sections in this exact order:

# Main Findings

Synthesise findings across all sections. For each major claim:
- State the specific numeric evidence
- Name the source (URL or title)
- Explain the technical significance
Use subsections per research section. No vague language.

# Comparative Analysis

Build at least one comparison table or structured comparison
between competing techniques, architectures, or implementations.
Format as a markdown table with measurable column headers.

# Trends

Identify directional patterns in the data.
Each trend must be backed by at least one specific data point.
No trend statement without evidence.

# Risks and Limitations

List specific failure modes, boundary conditions, and known limitations.
Include quantitative thresholds where available
(e.g. "SPWM efficiency degrades above M=0.786").

# Conclusion

Synthesise the technical verdict. What does the evidence support?
What remains unresolved? What trade-off does a practitioner face?

RULES:
- Do not invent facts, statistics, or dates
- Every numeric claim must be traceable to the summaries above
- Use precise technical language
- No filler phrases ("it is important to note", "in conclusion")
"""

# =============================================================
# WRITER PASS 2 — Executive summary derived LAST  (Priority 5)
# =============================================================

EXECUTIVE_SUMMARY_PROMPT = """
You have just read a dense technical research report on the topic below.
Now write a concise Executive Summary based ONLY on what the report says.

TOPIC:
{query}

REPORT BODY:
{body}

REQUIREMENTS:
- Maximum 200 words
- Must reference specific findings from the body (not generic claims)
- Must mention at least two quantitative results
- Must state the key tradeoff or design decision a practitioner faces
- Write in past tense (the research found / demonstrated / showed)
- No marketing language

FORMAT:
# Executive Summary

[your summary here]
"""
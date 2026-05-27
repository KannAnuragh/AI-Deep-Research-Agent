from app.llm import research_llm
from app.schemas import AdversarialOutput
from app.prompts import ADVERSARIAL_PROMPT
from app.utils.credibility import credibility_label


def adversarial_node(state):

    section = state["current_section"]
    sections = state.get("sections", [])
    summaries = state.get("summaries", {})
    search_results = state.get("search_results", [])

    # Find section description
    description = ""
    for s in sections:
        if s["name"] == section:
            description = s.get("description", "")
            break

    current_summary = summaries.get(section, "")

    # Build source manifest with credibility for the adversarial agent
    sources_manifest = ""
    for r in search_results:
        score = r.get("credibility_score", 0.5)
        label = credibility_label(score)
        sources_manifest += (
            f"  [{label} | {score:.2f}] "
            f"{r.get('title', 'Unknown')} "
            f"— {r.get('url', '')}\n"
        )

    prompt = ADVERSARIAL_PROMPT.format(
        section=section,
        description=description,
        summary=current_summary,
        sources=sources_manifest
    )

    response = research_llm.invoke_structured(
        AdversarialOutput,
        prompt
    )

    print(f"\nADVERSARIAL REVIEW FOR: {section}")
    print(f"  CONFIDENCE:  {response.overall_confidence:.2f}")
    print(f"  NEEDS MORE:  {response.requires_more_research}")

    if response.contradictions_found:
        print("  CONTRADICTIONS:")
        for c in response.contradictions_found:
            print(f"    - {c}")

    if response.unverified_benchmarks:
        print("  UNVERIFIED BENCHMARKS:")
        for b in response.unverified_benchmarks:
            print(f"    - {b}")

    if response.gaps_identified:
        print("  GAPS:")
        for g in response.gaps_identified[:3]:
            print(f"    - {g}")

    # Serialise findings into a structured text block for reflection
    parts = []

    if response.skeptic_findings:
        parts.append(
            "WEAK OR UNSUPPORTED CLAIMS:\n"
            + "\n".join(f"- {s}" for s in response.skeptic_findings)
        )

    if response.gaps_identified:
        parts.append(
            "IDENTIFIED GAPS:\n"
            + "\n".join(f"- {g}" for g in response.gaps_identified)
        )

    if response.contradictions_found:
        parts.append(
            "CONTRADICTIONS BETWEEN SOURCES:\n"
            + "\n".join(f"- {c}" for c in response.contradictions_found)
        )

    if response.unverified_benchmarks:
        parts.append(
            "BENCHMARKS WITHOUT CORROBORATION:\n"
            + "\n".join(f"- {b}" for b in response.unverified_benchmarks)
        )

    feedback_text = "\n\n".join(parts) if parts else "No major issues identified."

    return {
        "adversarial_feedback": feedback_text
    }
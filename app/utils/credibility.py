from urllib.parse import urlparse

# =========================
# DOMAIN CREDIBILITY SCORES
# =========================
# Score represents source trustworthiness (0.0–1.0)
# Based on: peer review, editorial standards, technical authority

DOMAIN_SCORES = {

    # IEEE — highest technical authority
    "ieeexplore.ieee.org": 0.95,
    "ieee.org": 0.92,

    # ACM
    "dl.acm.org": 0.93,
    "acm.org": 0.90,

    # Major academic publishers
    "sciencedirect.com": 0.90,
    "springer.com": 0.90,
    "springerlink.com": 0.88,
    "nature.com": 0.92,
    "wiley.com": 0.88,
    "tandfonline.com": 0.85,
    "iopscience.iop.org": 0.88,
    "pubs.acs.org": 0.88,

    # Open-access academic
    "arxiv.org": 0.82,
    "pmc.ncbi.nlm.nih.gov": 0.88,
    "ncbi.nlm.nih.gov": 0.87,
    "mdpi.com": 0.80,
    "akjournals.com": 0.78,
    "icrepq.com": 0.72,
    "ijirt.org": 0.65,
    "ijera.com": 0.65,
    "ijcseonline.org": 0.63,

    # Aggregators — variable quality
    "researchgate.net": 0.72,
    "academia.edu": 0.68,
    "semanticscholar.org": 0.75,

    # Vendor and technical docs — authoritative but biased
    "imperix.com": 0.72,
    "docs.amd.com": 0.73,
    "xilinx.com": 0.73,
    "intel.com": 0.73,
    "altera.com": 0.73,
    "mathworks.com": 0.70,
    "ti.com": 0.70,
    "analog.com": 0.70,
    "switchcraft.org": 0.62,

    # Standards bodies
    "iec.ch": 0.88,
    "ansi.org": 0.85,

    # Wikipedia — low trust for technical claims
    "en.wikipedia.org": 0.35,
    "wikipedia.org": 0.35,

    # Low-quality sources
    "homemade-circuits.com": 0.20,
    "youtube.com": 0.15,
    "scribd.com": 0.38,
    "medium.com": 0.32,
    "community.element14.com": 0.42,
    "proquest.com": 0.60,
}

# Fallback scores by pattern
EDU_SCORE = 0.80        # .edu / .ac. domains (university)
PDF_SCORE = 0.65        # bare PDFs without known domain
DEFAULT_SCORE = 0.50    # unknown domains

# =========================
# LABEL THRESHOLDS
# =========================

def credibility_label(score: float) -> str:
    if score >= 0.90:
        return "TIER-1 (peer-reviewed)"
    elif score >= 0.78:
        return "TIER-2 (academic/open-access)"
    elif score >= 0.65:
        return "TIER-3 (technical/vendor)"
    elif score >= 0.40:
        return "TIER-4 (aggregator/blog)"
    else:
        return "TIER-5 (low credibility)"


# =========================
# SCORING FUNCTION
# =========================

def score_url(url: str) -> float:
    """
    Return a credibility score (0.0–1.0) for a given URL.
    Higher = more trustworthy source.
    """

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

    except Exception:
        return DEFAULT_SCORE

    # Direct domain match
    if domain in DOMAIN_SCORES:
        return DOMAIN_SCORES[domain]

    # Subdomain match (e.g. etd.lib.metu.edu.tr → .edu)
    for known_domain, score in DOMAIN_SCORES.items():
        if domain.endswith("." + known_domain):
            return score

    # University / academic institution
    if ".edu" in domain or ".ac." in domain:
        return EDU_SCORE

    # Bare PDF (likely academic preprint or conference paper)
    if url.lower().endswith(".pdf"):
        return PDF_SCORE

    return DEFAULT_SCORE


def format_source_block(result: dict) -> str:
    """
    Format a search result with its credibility label
    for inclusion in prompts.
    """

    score = result.get("credibility_score", DEFAULT_SCORE)
    label = credibility_label(score)

    return (
        f"[{label} | score={score:.2f}]\n"
        f"TITLE: {result.get('title', 'Unknown')}\n"
        f"URL: {result.get('url', '')}\n"
        f"CONTENT:\n{result.get('content', '')}"
    )
from duckduckgo_search import DDGS

# Trusted domains
HIGH_QUALITY_DOMAINS = [
    "wikipedia.org",
    "ieee.org",
    "arxiv.org",
    "nature.com",
    "sciencedirect.com",
    "mit.edu",
    "stanford.edu",
    "openai.com",
    "deepmind.com",
]

def is_high_quality(url: str):

    if not url:
        return False

    return any(domain in url for domain in HIGH_QUALITY_DOMAINS)

def search_web(query: str):

    results = DDGS().text(
        query,
        max_results=10
    )

    seen_urls = set()
    filtered_results = []

    # First pass → prioritize trusted domains
    for r in results:

        url = r.get("href")

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        formatted = {
            "title": r.get("title"),
            "content": r.get("body"),
            "url": url
        }

        if is_high_quality(url):
            filtered_results.append(formatted)

    # Second pass → fill remaining slots
    if len(filtered_results) < 5:

        for r in DDGS().text(query, max_results=10):

            url = r.get("href")

            if not url:
                continue

            formatted = {
                "title": r.get("title"),
                "content": r.get("body"),
                "url": url
            }

            if formatted not in filtered_results:
                filtered_results.append(formatted)

            if len(filtered_results) >= 5:
                break

    return filtered_results[:5]
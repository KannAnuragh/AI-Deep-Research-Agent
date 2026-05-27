from ddgs import DDGS

from app.tools.web_extract import extract_webpage
from app.utils.credibility import score_url, credibility_label


def worker_node(state):

    queries = state.get("search_queries", [])
    section = state.get("current_section", "")

    # Fallback if planner produced nothing
    if not queries:
        queries = [section]

    all_results = []
    seen_urls = set()

    for query in queries:

        print(f"\nSEARCHING: {query}\n")

        try:
            results = DDGS().text(query, max_results=2)
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
            continue

        if not results:
            continue

        for r in results:

            url = r.get("href")

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            # Score source credibility before extracting
            cred_score = score_url(url)
            cred_label = credibility_label(cred_score)

            print(f"EXTRACTING [{cred_label} | {cred_score:.2f}]: {url}")

            try:
                content = extract_webpage(url)
            except Exception as e:
                print(f"Extraction failed: {e}")
                content = None

            # Fallback to search snippet
            if not content:
                content = r.get("body", "")

            if not content:
                continue

            all_results.append({
                "title": r.get("title", ""),
                "content": content[:1500],
                "url": url,
                "credibility_score": cred_score,
            })

    # Accumulate with rolling window, preserve highest-credibility results
    existing = state.get("search_results", [])
    combined = existing + all_results

    # Sort by credibility descending before capping, so we keep best sources
    combined.sort(
        key=lambda x: x.get("credibility_score", 0.0),
        reverse=True
    )
    combined = combined[:10]

    print(
        f"\nWORKER: {len(all_results)} new results "
        f"({len(combined)} total) for '{section}'\n"
    )

    return {
        "search_results": combined,
        "iteration_count": state.get("iteration_count", 0) + 1,
    }
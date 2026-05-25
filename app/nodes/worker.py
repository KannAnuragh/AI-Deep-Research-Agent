from ddgs import DDGS


def worker_node(state):

    queries = state.get("search_queries", [])
    section = state.get("current_section", "")

    # Fallback: search the section name if no queries were planned
    if not queries:
        queries = [section]

    all_results = []
    seen_urls = set()

    for query in queries:

        try:
            results = DDGS().text(
                query,
                max_results=5
            )
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
            continue

        if not results:
            continue

        for r in results:

            url = r.get("href")

            if not url:
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            all_results.append({
                "title": r.get("title"),
                "content": r.get("body"),
                "url": url
            })

    # Accumulate results across iterations, keep latest 40
    existing = state.get("search_results", [])
    combined = (existing + all_results)[-40:]

    print(
        f"\nWORKER: {len(all_results)} new results "
        f"({len(combined)} total) for '{section}'\n"
    )

    return {
        "search_results": combined,
        "iteration_count": state.get("iteration_count", 0) + 1
    }
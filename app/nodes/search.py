from ddgs import DDGS

def search_node(state):

    queries = state["search_queries"]

    all_results = []
    seen_urls = set()

    for query in queries:

        try:
            results = DDGS().text(
                query,
                max_results=5
            )
        except Exception as e:
            print(f"Search failed for {query}: {e}")
            continue

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

            all_results.append(formatted)

    return {
        "search_results": all_results
    }
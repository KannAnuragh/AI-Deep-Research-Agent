from ddgs import DDGS

from app.tools.web_extract import (
    extract_webpage
)


def worker_node(state):

    queries = state.get(
        "search_queries",
        []
    )

    section = state.get(
        "current_section",
        ""
    )

    # Fallback
    if not queries:
        queries = [section]

    all_results = []

    seen_urls = set()

    for query in queries:

        print(f"\nSEARCHING: {query}\n")

        try:

            results = DDGS().text(
                query,
                max_results=2
            )

        except Exception as e:

            print(
                f"Search failed "
                f"for '{query}': {e}"
            )

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

            print(
                f"EXTRACTING: {url}"
            )

            try:

                content = extract_webpage(
                    url
                )

            except Exception as e:

                print(
                    f"Extraction failed: {e}"
                )

                continue

            # fallback to snippet
            if not content:

                content = r.get(
                    "body",
                    ""
                )

            if not content:
                continue

            all_results.append({

                "title": r.get(
                    "title",
                    ""
                ),

                "content": content[:1500],

                "url": url
            })

    # Preserve rolling memory
    existing = state.get(
        "search_results",
        []
    )

    combined = (existing + all_results)[-10:]

    print(
        f"\nWORKER:"
        f" {len(all_results)} new results "
        f"({len(combined)} total)"
        f" for '{section}'\n"
    )

    return {

        "search_results": combined,

        "iteration_count":
            state.get(
                "iteration_count",
                0
            ) + 1
    }
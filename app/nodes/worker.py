from ddgs import DDGS

def worker_node(state):

    section = state["current_section"]

    results = DDGS().text(
        section,
        max_results=10
    )

    formatted_results = []

    for r in results:

        formatted_results.append({
            "title": r.get("title"),
            "content": r.get("body"),
            "url": r.get("href")
        })

    return {
        "search_results": formatted_results
    }
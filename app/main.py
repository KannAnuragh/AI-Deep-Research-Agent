from app.nodes.planner import generate_search_queries
from app.nodes.search import search_web
from app.nodes.summarizer import summarize_results
from app.nodes.writer import generate_report

def run_research(query):

    print(f"\nResearch Topic: {query}")

    # Step 1 — Generate queries
    queries = generate_search_queries(query)

    print("\nGenerated Search Queries:")
    for q in queries:
        print("-", q)

    all_summaries = []

    # Step 2 — Search + summarize



    for q in queries:
        try:
            results = search_web(q)
        except Exception as e:
            print(f"Search failed: {e}")
            continue

        print(f"\nSearching: {q}")


        try:
            summary = summarize_results(q, results)
            all_summaries.append(summary)
        except Exception as e:
            print(f"Summarization failed: {e}")

    # Step 3 — Final report
    report = generate_report(query, all_summaries)

    return report

if __name__ == "__main__":

    query = input("Enter research topic: ")

    final_report = run_research(query)

    print("\nFINAL REPORT:\n")
    print(final_report)
from app.llm import research_llm

def compressor_node(state):

    results = state["search_results"]

    compressed = []

    for r in results:

        prompt = f"""
Compress this technical content into
5 concise bullet points.

CONTENT:
{r['content'][:3000]}
"""

        response = research_llm.invoke(
            prompt
        )

        compressed.append({

            "title": r["title"],

            "content": str(
                response.content
            ),

            "url": r["url"]
        })

    return {
        "search_results": compressed
    }
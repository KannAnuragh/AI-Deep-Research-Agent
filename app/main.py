from graph import graph

if __name__ == "__main__":

    query = input("Enter research topic: ")

    result = graph.invoke(
        {
            "user_query": query
        },
        debug=True
    )

    print("\nFINAL REPORT:\n")

    print(result["final_report"])
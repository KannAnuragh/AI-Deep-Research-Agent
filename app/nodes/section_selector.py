def section_selector_node(state):

    sections = state.get("sections", [])

    summaries = state.get("summaries", {})

    if not sections:

        return {
            "current_section": "General Research"
        }

    # Find unfinished section
    for section in sections:

        name = section["name"]

        if name not in summaries:

            print(f"\nCURRENT SECTION: {name}")

            return {
                "current_section": name
            }

    # fallback
    return {
        "current_section": sections[0]["name"]
    }
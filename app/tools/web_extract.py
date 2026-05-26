import trafilatura


def extract_webpage(url):

    downloaded = trafilatura.fetch_url(
        url
    )

    if not downloaded:
        return None

    text = trafilatura.extract(
        downloaded,
        include_links=False
    )

    return text
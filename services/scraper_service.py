import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SEARCH_URL = "https://www.google.com/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def scrape_resources(query: str, max_pages: int = 2) -> list[dict]:
    results = []

    for page in range(max_pages):
        try:
            params = {"q": f"{query} study notes PDF", "start": page * 10}
            response = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for link_tag in soup.find_all("a", href=True):
                href = link_tag["href"]
                if not _is_relevant_link(href):
                    continue

                title = link_tag.get_text(strip=True) or href.split("/")[-1]
                results.append({
                    "title": title[:120],
                    "description": f"Resource found for: {query}",
                    "views": 0,
                    "link": href,
                    "thumbnail": "",
                    "source": "web",
                })

        except requests.RequestException:
            continue

    seen = set()
    unique = []
    for r in results:
        if r["link"] not in seen:
            seen.add(r["link"])
            unique.append(r)

    return unique[:15]


def _is_relevant_link(href: str) -> bool:
    if not href.startswith("http"):
        return False
    irrelevant = ["google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com"]
    return not any(domain in href for domain in irrelevant)

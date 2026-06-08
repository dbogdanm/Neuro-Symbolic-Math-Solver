import re

import requests
from duckduckgo_search import DDGS


def _fallback_html_search(query: str, max_results: int) -> list:
    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    data = {"q": query}
    results = []
    try:
        r = requests.post(url, data=data, headers=headers, timeout=10)
        if r.status_code == 200:
            snippets = re.findall(
                r'<a class="result__snippet[^>]*>(.*?)</a>',
                r.text,
                re.DOTALL | re.IGNORECASE,
            )
            for s in snippets:
                clean_snippet = re.sub(r'<[^>]+>', '', s).strip()
                if clean_snippet:
                    results.append(f"BODY: {clean_snippet}")
    except Exception as e:
        print(f"  [HTML Fallback Error]: {e}")
    return results[:max_results]

def get_web_hint(query: str, max_results: int = 3) -> str:
    """
    Final attempt at robust search.
    Tries basic text search and news search, with a raw HTML scraper fallback.
    """
    if not query:
        return ""

    results_list = []
    q = query.strip()

    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(q, max_results=max_results))
            for r in search_results:
                results_list.append(f"TITLE: {r.get('title')}\nBODY: {r.get('body')}\n")
    except Exception as e:
        print(f"  [Text Search Error]: {e}")

    if not results_list:
        try:
            with DDGS() as ddgs:
                news_results = list(ddgs.news(q, max_results=max_results))
                for r in news_results:
                    results_list.append(f"NEWS: {r.get('title')}\nBODY: {r.get('body')}\n")
        except Exception as e:
            print(f"  [News Search Error]: {e}")

    if not results_list:
        print("  [Web Search] Library failed, falling back to HTML scraper...")
        html_results = _fallback_html_search(q, max_results=max_results)
        for r in html_results:
            results_list.append(f"{r}\n")

    if not results_list:
        return ""

    combined = "\n".join(results_list[:max_results])
    return f"WEB SEARCH RESULTS:\n{combined}"

if __name__ == "__main__":
    print(get_web_hint("US President current"))

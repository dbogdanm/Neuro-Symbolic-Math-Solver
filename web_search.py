from duckduckgo_search import DDGS
import time
from typing import List

def get_web_hint(query: str, max_results: int = 3) -> str:
    """
    Final attempt at robust search.
    Tries basic text search and news search.
    """
    if not query:
        return ""
    
    results_list = []
    
    # Simple query cleaning
    q = query.strip()
    
    try:
        with DDGS() as ddgs:
            # Try text search first
            # We don't specify region to avoid strict blocking, 
            # but we trust DDG to handle it.
            search_results = list(ddgs.text(q, max_results=max_results))
            for r in search_results:
                results_list.append(f"TITLE: {r.get('title')}\nBODY: {r.get('body')}\n")
    except Exception as e:
        print(f"  [Text Search Error]: {e}")

    if not results_list:
        try:
            with DDGS() as ddgs:
                # Try news search as fallback
                news_results = list(ddgs.news(q, max_results=max_results))
                for r in news_results:
                    results_list.append(f"NEWS: {r.get('title')}\nBODY: {r.get('body')}\n")
        except Exception as e:
            print(f"  [News Search Error]: {e}")

    if not results_list:
        return ""
            
    combined = "\n".join(results_list[:max_results])
    return f"WEB SEARCH RESULTS:\n{combined}"

if __name__ == "__main__":
    print(get_web_hint("US President current"))

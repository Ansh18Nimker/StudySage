def rank_results(results: list[dict], query: str) -> list[dict]:
    if not results:
        return []

    keywords = query.lower().split()
    max_views = max((r.get("views", 0) for r in results), default=1) or 1

    for result in results:
        text = f"{result['title']} {result['description']}".lower()
        keyword_matches = sum(1 for kw in keywords if kw in text)
        keyword_score = keyword_matches / len(keywords) if keywords else 0

        views_score = result.get("views", 0) / max_views

        result["score"] = round((keyword_score * 0.5) + (views_score * 0.3), 4)

    results.sort(key=lambda r: r["score"], reverse=True)
    return results

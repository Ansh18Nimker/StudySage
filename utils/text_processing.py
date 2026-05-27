import re


def clean_query(query: str) -> str:
    query = query.strip().lower()
    query = re.sub(r"\s+", " ", query)
    return query

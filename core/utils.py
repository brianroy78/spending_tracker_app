def is_empty(obj) -> bool:
    return len(obj) == 0


def split_keywords(keywords: str) -> list[str]:
    return keywords.split("|")

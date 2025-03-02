import re


def remove_hash_from_titles(text: str) -> str:
    return re.sub(r"^\s*#+\s*(.*)$", r"\1", text, flags=re.MULTILINE)


def format_response_chunk(text: str) -> str:
    return remove_hash_from_titles(text)

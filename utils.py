import re


def get_video_id(url: str) -> str | None:
    """Extracts a Youtube video's id from its url"""
    regexp = r"^.*v=([a-zA-Z0-9]+)$"
    match = re.search(regexp, url)

    if match:
        return match.group(1)

    return None

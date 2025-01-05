import re

from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url: str) -> str | None:
    """Extracts a Youtube video's id from its url"""
    regexp = r"^.*v=([a-zA-Z0-9]+)$"
    match = re.search(regexp, url)

    if match:
        return match.group(1)

    return None


def get_video_transcript(video_id: str):
    """Gets the transcript of YouTube video from its id"""
    return YouTubeTranscriptApi.get_transcript(video_id)


def join_transcript(transcript: list) -> str:
    full_text = ""

    for element in transcript:
        for key, val in element.items():
            if key == "text":
                full_text += f" {val}"

    return full_text

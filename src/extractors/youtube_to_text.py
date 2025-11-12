"""Extract transcripts from YouTube videos."""

from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]*)',
        r'youtube\.com\/embed\/([^&\n?]*)',
        r'youtube\.com\/v\/([^&\n?]*)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_transcript(video_id: str) -> str:
    """Extract transcript from YouTube video."""
    transcript_obj = YouTubeTranscriptApi().fetch(video_id)
    full_text = ' '.join([snippet.text for snippet in transcript_obj])
    formatted_text = full_text.replace('. ', '.\n')
    return formatted_text
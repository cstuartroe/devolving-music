import requests
import os
from typing import Optional

API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_youtube_playlist_items(playlist_id: str, page_token: Optional[str] = None):
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "key": API_KEY,
        "maxResults": 50,
    }

    if page_token:
        params["pageToken"] = page_token

    data = requests.get(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        params=params
    ).json()

    yield from data["items"]
    if data.get("nextPageToken"):
        yield from get_youtube_playlist_items(playlist_id, page_token=data["nextPageToken"])


def get_video_data(video_id: str):
    params = {
        "part": "snippet",
        "id": video_id,
        "key": API_KEY,
    }

    data = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params=params,
    ).json()

    return data["items"][0]


def get_youtube_playlist_videos(playlist_id: str):
    return [
        get_video_data(item["contentDetails"]["videoId"])
        for item
        in get_youtube_playlist_items(playlist_id)
    ]

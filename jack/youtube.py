import os

from apiclient.discovery import build


DEVELOPER_KEY = os.environ['YOUTUBE_API_ACCESS_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_build():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def search_channel(query):
    youtube = youtube_build()

    response = youtube.search().list(
        part="id,snippet",
        q=query,
        type='channel'
    ).execute()

    return response["items"]


def search_video_in_channel(channel_id, query):
    youtube = youtube_build()

    response = youtube.search().list(
        channelId=channel_id,
        part="id,snippet",
        q=query,
        type='video'
    ).execute()

    return response["items"]
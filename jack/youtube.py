import os

from apiclient.discovery import build


DEVELOPER_KEY = os.environ['YOUTUBE_API_ACCESS_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_build():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def youtube_search(type, query):
    youtube = youtube_build()

    response = youtube.search().list(
        part="id,snippet",
        q=query,
        type=type
    ).execute()

    print(response["items"])

    return response["items"]
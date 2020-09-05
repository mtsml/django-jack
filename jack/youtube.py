import os

from apiclient.discovery import build


DEVELOPER_KEY = os.environ['YOUTUBE_API_ACCESS_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_build():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def search_youtube(query):
    youtube = youtube_build()

    response = youtube.search().list(
        maxResults=50,
        part="id,snippet",
        q=query,
        type='channel,video'
    ).execute()

    channel_list =[]
    video_list = []
    print(response["items"])
    for item in response["items"]:
        if item["id"]["kind"] == "youtube#channel":
            channel_list.append(item)
        elif item["id"]["kind"] == "youtube#video":
            video_list.append(item)

    result = {
        'channel_list': channel_list,
        'video_list': video_list
    }
    return result


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
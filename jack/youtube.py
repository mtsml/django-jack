import os

from apiclient.discovery import build

from .models import Channel, Video


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
    for item in response["items"]:
        if item["id"]["kind"] == "youtube#channel":
            registered = False
            if Channel.is_channel_id_exists(item["id"]["channelId"]):
                registered = True
            channel_list.append({
                'channel_id': item["id"]["channelId"],
                'thumbnails_url': item["snippet"]["thumbnails"]["default"]["url"],
                'channel_nm': item["snippet"]["title"],
                'registered': registered
            })
        elif item["id"]["kind"] == "youtube#video":
            registered = False
            if Video.is_video_id_exists(item["id"]["videoId"]):
                registered = True
            video_list.append({
                'video_id': item["id"]["videoId"],
                'thumbnails_url': item["snippet"]["thumbnails"]["default"]["url"],
                'video_nm': item["snippet"]["title"],
                'channel_id': item["snippet"]["channelId"],
                'channel_nm': item["snippet"]["channelTitle"],
                'registered': registered
            })

    result = {
        'channel_list': channel_list,
        'video_list': video_list
    }
    return result
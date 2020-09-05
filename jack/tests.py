import datetime

from django.test import TestCase
from django.urls import reverse

from .models import Channel, Comment


CHANNEL_ID = 'TokaiOnAir'
CHANNEL_NM = '東海オンエア'
CHANNEL_ID_INVALID = 'TokaiOnAirJanai'
CHANNEL_NM_INVALID = '東海オンエアじゃない'
VIDEO_ID = 'mP6WW_BHsaA'
COMMENT = 'カントゥーヤ！'


class IndexViewTests(TestCase):
    def test_display_channel(self):
        """
        テーブルにチャンネルが存在する場合は、チャンネルの一覧が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['channel_list'], 
            [f'<Channel: {CHANNEL_ID}>']
        )

    def test_add_exist_channel(self):
        """
        既に塘路作されているチャンネルを追加の場合は、テーブルにオブジェクトが追加しない
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.post('/', {
            'channel_id': CHANNEL_ID, 
            'channel_nm': CHANNEL_NM,
            'add_channel': ['']
        })
        self.assertQuerysetEqual(
            Channel.objects.all(),
            [f'<Channel: {CHANNEL_ID}>']
        )


# class SearchViewTests(TestCase):
#     def test_no_channel(self):
#         """
#         テーブルにチャンネルが存在しない場合は、メッセージが表示される
#         """
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'No Recomended Youtuber.')
#         self.assertQuerysetEqual(response.context['channel_list'], [])

#     def test_display_channel(self):
#         """
#         テーブルにチャンネルが存在する場合は、チャンネルの一覧が表示される
#         """
#         channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
#         response = self.client.get(reverse('index'))
#         self.assertQuerysetEqual(
#             response.context['channel_list'], 
#             [f'<Channel: {CHANNEL_ID}>']
#         )

#     def test_add_channel(self):
#         """
#         チャンネルを追加すると、テーブルにオブジェクトが追加される
#         """
#         response = self.client.post('/', {
#             'channel_id': CHANNEL_ID, 
#             'channel_nm': CHANNEL_NM,
#             'add_channel': ['']
#         })
#         self.assertQuerysetEqual(
#             Channel.objects.all(),
#             [f'<Channel: {CHANNEL_ID}>']
#         )

#     def test_add_exist_channel(self):
#         """
#         既に塘路作されているチャンネルを追加の場合は、テーブルにオブジェクトが追加しない
#         """
#         channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
#         response = self.client.post('/', {
#             'channel_id': CHANNEL_ID, 
#             'channel_nm': CHANNEL_NM,
#             'add_channel': ['']
#         })
#         self.assertQuerysetEqual(
#             Channel.objects.all(),
#             [f'<Channel: {CHANNEL_ID}>']
#         )


class ChannelViewTests(TestCase):
    def test_no_channel(self):
        """
        テーブルにチャンネルが存在しない場合は、404エラー
        """
        response = self.client.get(f'/channel/{CHANNEL_ID_INVALID}/')
        self.assertEqual(response.status_code, 404)

    def test_display_channel(self):
        """
        テーブルにチャンネルが存在する場合は、チャンネルの詳細が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.get(f'/channel/{CHANNEL_ID}/')
        self.assertQuerysetEqual(
            [response.context['channel']], 
            [f'<Channel: {CHANNEL_ID}>']
        )
    
    def test_display_video(self):
        """
        テーブルにチャンネルに紐づくビデオが存在する場合は、ビデオの一覧が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.get(f'/channel/{CHANNEL_ID}/')
        self.assertQuerysetEqual(
            response.context['video_list'], 
            [f'<Video: {VIDEO_ID}>']
        )

    def test_display_channel_comment(self):
        """
        チャンネルに紐づくコメントが存在する場合は、コメントの一覧が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        comment = Comment.objects.create(category='channel', foreign_id=CHANNEL_ID, comment=COMMENT, reg_datetime=datetime.datetime.now())
        response = self.client.get(f'/channel/{CHANNEL_ID}/')
        self.assertContains(response, COMMENT)

    def test_add_channel_comment(self):
        """
        チャンネルにコメントを追加すると、テーブルにオブジェクトが作成される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.post(f'/channel/{CHANNEL_ID}/', {
            'comment': COMMENT,
            'add_comment': ['']
        })
        self.assertQuerysetEqual(
            Comment.objects.all(),
            [f'<Comment: channel:{CHANNEL_ID}>']
        )


class VideoViewTests(TestCase):
    def test_no_video(self):
        """
        テーブルに動画が存在しない場合は、404エラー
        """
        response = self.client.get(f'/video/{VIDEO_ID}/')
        self.assertEqual(response.status_code, 404)

    def test_display_video(self):
        """
        テーブルに動画が存在する場合は、動画の詳細が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.get(f'/video/{VIDEO_ID}/')
        self.assertQuerysetEqual(
            [response.context['video']], 
            [f'<Video: {VIDEO_ID}>']
        )

    def test_display_comment(self):
        """
        テーブルに動画のコメントが存在する場合は、コメントが表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        comment = Comment.objects.create(category='video', foreign_id=VIDEO_ID, comment=COMMENT, reg_datetime=datetime.datetime.now())
        response = self.client.get(f'/video/{VIDEO_ID}/')
        self.assertContains(response, COMMENT)

    def test_add_video_comment(self):
        """
        動画にコメントを追加すると、テーブルにオブジェクトが作成される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.post(f'/video/{VIDEO_ID}/', {
            'comment': COMMENT,
            'add_comment': ['']
        })
        self.assertQuerysetEqual(
            Comment.objects.all(),
            [f'<Comment: video:{VIDEO_ID}>']
        )
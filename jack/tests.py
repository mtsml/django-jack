import datetime
import json

from django.test import TestCase
from django.urls import reverse

from .models import Channel, Comment


CHANNEL_ID = 'TokaiOnAir'
CHANNEL_NM = '東海オンエア'
CHANNEL_ID_INVALID = 'TokaiOnAirJanai'
CHANNEL_NM_INVALID = '東海オンエアじゃない'
VIDEO_ID = 'mP6WW_BHsaA'
VIDEO_NM = 'ラタトゥイユ'
COMMENT = 'カントゥーヤ！'
THUMBNAILS_URL = 'url'


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

    def test_display_video(self):
        """
        テーブルに動画が存在する場合は、動画の一覧が表示される
        最新動画（new_video_list）: 登録日の降順
        人気動画（popular_video_list）: コメント数の降順
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video1 = channel.video_set.create(video_id=VIDEO_ID, video_nm=VIDEO_NM, reg_datetime=datetime.datetime.now())
        video2 = channel.video_set.create(video_id=f'{VIDEO_ID}2', video_nm=VIDEO_NM, reg_datetime=datetime.datetime.now())
        comment = Comment.objects.create(category='video', foreign_id=VIDEO_ID, comment=COMMENT, reg_datetime=datetime.datetime.now())
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['new_video_list'], 
            [f'<Video: {VIDEO_ID}2>', f'<Video: {VIDEO_ID}>']
        )
        self.assertQuerysetEqual(
            response.context['popular_video_list'], 
            [f'<Video: {VIDEO_ID}>', f'<Video: {VIDEO_ID}2>']
        )


class SearchViewTests(TestCase):
    def test_add_channel(self):
        """
        チャンネルを追加すると、テーブルにオブジェクトが追加される
        """
        response = self.client.post(reverse('search'), {
            'channel_id': CHANNEL_ID, 
            'channel_nm': CHANNEL_NM,
            'thumbnails_url': THUMBNAILS_URL,
            'add_channel': ['']
        })
        self.assertQuerysetEqual(
            Channel.objects.all(),
            [f'<Channel: {CHANNEL_ID}>']
        )

    def test_add_exist_channel(self):
        """
        既に作成されているチャンネルの場合は、テーブルにオブジェクトを追加しない
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.post(reverse('search'), {
            'channel_id': CHANNEL_ID, 
            'channel_nm': CHANNEL_NM,
            'thumbnails_url': THUMBNAILS_URL,
            'add_channel': ['']
        })
        self.assertQuerysetEqual(
            Channel.objects.all(),
            [f'<Channel: {CHANNEL_ID}>']
        )


class ChannelViewTests(TestCase):
    def test_no_channel(self):
        """
        テーブルにチャンネルが存在しない場合は、404エラー
        """
        response = self.client.get(reverse('channel', args=[CHANNEL_ID]))
        self.assertEqual(response.status_code, 404)

    # def test_display_video(self):
    #     """
    #     テーブルにチャンネルに紐づくビデオが存在する場合は、ビデオの一覧が表示される
    #     最新動画（new_video_list）: 登録日の降順
    #     人気動画（popular_video_list）: コメント数の降順
    #     """
    #     channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
    #     channel2 = Channel.objects.create(channel_id=f'{CHANNEL_ID}2', channel_nm=CHANNEL_NM)
    #     video1 = channel.video_set.create(video_id=VIDEO_ID, video_nm=VIDEO_NM, reg_datetime=datetime.datetime.now())
    #     video2 = channel.video_set.create(video_id=f'{VIDEO_ID}2', video_nm=VIDEO_NM, reg_datetime=datetime.datetime.now())
    #     video3 = channel2.video_set.create(video_id=f'{VIDEO_ID}3', video_nm=VIDEO_NM, reg_datetime=datetime.datetime.now())
    #     comment = Comment.objects.create(category='video', foreign_id=VIDEO_ID, comment=COMMENT, reg_datetime=datetime.datetime.now())
    #     response = self.client.get(reverse('channel', args=[CHANNEL_ID]))
    #     self.assertQuerysetEqual(
    #         response.context['new_video_list'], 
    #         [f'<Video: {VIDEO_ID}2>', f'<Video: {VIDEO_ID}>']
    #     )
    #     self.assertQuerysetEqual(
    #         response.context['popular_video_list'], 
    #         [f'<Video: {VIDEO_ID}>', f'<Video: {VIDEO_ID}2>']
    #     )


class VideoViewTests(TestCase):
    def test_no_video(self):
        """
        テーブルに動画が存在しない場合は、404エラー
        """
        response = self.client.get(reverse('video', args=[VIDEO_ID]))
        self.assertEqual(response.status_code, 404)

    def test_display_video(self):
        """
        テーブルに動画が存在する場合は、動画の詳細が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.get(reverse('video', args=[VIDEO_ID]))
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
        response = self.client.get(reverse('video', args=[VIDEO_ID]))
        content = json.loads(response.content)
        self.assertIn(
            COMMENT,
            content["video_player_html"]
        )

    def test_add_video_comment(self):
        """
        動画にコメントを追加すると、テーブルにオブジェクトが作成される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.post(reverse('video', args=[VIDEO_ID]), {
            'comment': COMMENT,
            'add_comment': ['']
        })
        self.assertQuerysetEqual(
            Comment.objects.all(),
            [f'<Comment: video:{VIDEO_ID}>']
        )
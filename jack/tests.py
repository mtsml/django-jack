import datetime

from django.test import TestCase
from django.urls import reverse

from .models import Channel, Comment
from .forms import VIDEO_URL_PREFIX


CHANNEL_ID = 'TokaiOnAir'
CHANNEL_NM = '東海オンエア'
CHANNEL_ID_INVALID = 'TokaiOnAirJanai'
CHANNEL_NM_INVALID = '東海オンエアじゃない'
VIDEO_ID = 'mP6WW_BHsaA'
COMMENT = 'カントゥーヤ！'


class IndexViewTests(TestCase):
    def test_no_channel(self):
        """
        テーブルにチャンネルが存在しない場合は、メッセージが表示される
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Recomended Youtuber.')
        self.assertQuerysetEqual(response.context['channel_list'], [])

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

    def test_add_channel(self):
        """
        チャンネルを追加すると、テーブルにオブジェクトが追加される
        """
        response = self.client.post('/', {
            'channel_id': CHANNEL_ID, 
            'channel_nm': CHANNEL_NM,
            'add_channel': ['']
        })
        self.assertQuerysetEqual(
            Channel.objects.all(),
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


class DetailViewTests(TestCase):
    def test_no_channel(self):
        """
        テーブルにチャンネルが存在しない場合は、404エラー
        """
        response = self.client.get(f'/{CHANNEL_ID_INVALID}/')
        self.assertEqual(response.status_code, 404)

    def test_display_channel(self):
        """
        テーブルにチャンネルが存在する場合は、チャンネルの詳細が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.get(f'/{CHANNEL_ID}/')
        self.assertQuerysetEqual(
            [response.context['channel']], 
            [f'<Channel: {CHANNEL_ID}>']
        )
    
    def test_no_video(self):
        """
        テーブルにチャンネルに紐づくビデオが存在しない場合は、何も表示されない
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.get(f'/{CHANNEL_ID}/')
        self.assertQuerysetEqual(response.context['video_list'], [])

    def test_display_video(self):
        """
        テーブルにチャンネルに紐づくビデオが存在する場合は、ビデオの一覧が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.get(f'/{CHANNEL_ID}/')
        self.assertQuerysetEqual(
            response.context['video_list'], 
            [f'<Video: {VIDEO_ID}>']
        )

    def test_add_video(self):
        """
        動画を追加すると、テーブルにオブジェクトが追加され、リダイレクトされる
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        response = self.client.post(f'/{CHANNEL_ID}/', {
            'video_id': {VIDEO_ID},
            'add_video': ['']
        })
        self.assertQuerysetEqual(
            channel.video_set.all(),
            [f'<Video: {VIDEO_ID}>']
        )

    def test_display_video_comment(self):
        """
        動画に紐づくコメントが存在する場合は、コメントの一覧が表示される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        comment = Comment.objects.create(category='video', foreign_id=VIDEO_ID, comment=COMMENT, reg_datetime=datetime.datetime.now())
        response = self.client.get(f'/{CHANNEL_ID}/')
        self.assertContains(response, COMMENT)

    def test_add_video_comment(self):
        """
        動画にコメントを追加すると、テーブルにオブジェクトが作成される
        """
        channel = Channel.objects.create(channel_id=CHANNEL_ID, channel_nm=CHANNEL_NM)
        video = channel.video_set.create(video_id=VIDEO_ID)
        response = self.client.post(f'/{CHANNEL_ID}/', {
            'video_id': VIDEO_ID,
            'comment': COMMENT,
            'add_comment': ['']
        })
        self.assertQuerysetEqual(
            Comment.objects.all(),
            [f'<Comment: video:{VIDEO_ID}>']
        )
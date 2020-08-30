from django.test import TestCase
from django.urls import reverse

from .models import Channel


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
        channel_id = 'TokaiOnAir'
        channel = Channel.objects.create(channel_id=channel_id, channel_nm='東海オンエア')
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['channel_list'], 
            [f'<Channel: {channel_id}>']
        )

    def test_add_channel(self):
        """
        チャンネルを追加すると、テーブルにオブジェクトが追加され、リダイレクトされる
        """
        channel_id = 'TokaiOnAir'
        response = self.client.post('/', {'channel_id': channel_id, 'channel_nm': '東海オンエア'})
        self.assertQuerysetEqual(
            Channel.objects.all(),
            [f'<Channel: {channel_id}>']
        )
        self.assertEqual(response.status_code, 302)

    def test_add_invalid_channel(self):
        """
        追加しようとしたチャンネルが実在しない場合、テーブルにオブジェクトは作成されず、エラーメッセージが表示されれる
        """
        channel_id = 'TokaiOnAirJanai'
        response = self.client.post('/', {'channel_id': channel_id, 'channel_nm': '東海オンエアじゃない'})
        self.assertContains(response, 'そのチャンネルIDは存在しません')
        self.assertQuerysetEqual(response.context['channel_list'], [])


class DetailViewTests(TestCase):
    def test_no_channel(self):
        """
        テーブルにチャンネルが存在しない場合は、404エラー
        """
        response = self.client.get('/TokaiOnAirJanai/')
        self.assertEqual(response.status_code, 404)

    def test_display_channel(self):
        """
        テーブルにチャンネルが存在する場合は、チャンネルの詳細が表示される
        """
        channel_id = 'TokaiOnAir'
        channel = Channel.objects.create(channel_id=channel_id, channel_nm='東海オンエア')
        response = self.client.get(f'/{channel_id}/')
        self.assertQuerysetEqual(
            [response.context['channel']], 
            [f'<Channel: {channel_id}>']
        )
    
    def test_no_video(self):
        """
        テーブルにチャンネルに紐づくビデオが存在しない場合は、何も表示されない
        """
        channel_id = 'TokaiOnAir'
        channel = Channel.objects.create(channel_id=channel_id, channel_nm='東海オンエア')
        response = self.client.get(f'/{channel_id}/')
        self.assertQuerysetEqual(response.context['video_list'], [])

    def test_display_video(self):
        """
        テーブルにチャンネルに紐づくビデオが存在する場合は、ビデオの一覧が表示される
        """
        channel_id = 'TokaiOnAir'
        channel = Channel.objects.create(channel_id=channel_id, channel_nm='東海オンエア')
        video_id = 'mP6WW_BHsaA'
        video = channel.video_set.create(video_id=video_id)
        response = self.client.get(f'/{channel_id}/')
        self.assertQuerysetEqual(
            response.context['video_list'], 
            [f'<Video: {video_id}>']
        )
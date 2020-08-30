from django import forms
import urllib3

from .models import Channel, Video


VIDEO_URL_PREFIX = 'https://www.youtube.com/watch?v='


def get_video_id_from_url(url):
    return url.replace(VIDEO_URL_PREFIX, '')


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ('channel_id', 'channel_nm')
        labels = {
            'channel_id': 'チャンネルID',
            'channel_nm': 'チャンネル名'
        }

    def clean_channel_id(self):
        channel_id = self.cleaned_data['channel_id']
        if not self.is_valid_channel_id(channel_id):
            raise forms.ValidationError('invalid channel id')
        return channel_id

    def is_valid_channel_id(self, channel_id):
        url = f'https://www.youtube.com/user/{channel_id}/'
        r = urllib3.PoolManager().request('GET', url)
        if r.status == 200:
            return True
        else:
            return False


class VideoForm(forms.Form):
    url = forms.CharField()

    def clean_url(self):
        url = self.cleaned_data['url']
        if not self.is_valid_video_url(url):
            raise forms.ValidationError('invalid video url')
        return url

    """
    動画IDが不正な場合もTrueで返してしまう
    レスポンスをパースするかAPIを使うべき
    """    
    def is_valid_video_url(self, url):
        if url.startswith(VIDEO_URL_PREFIX):
            return True
        else:
            return False
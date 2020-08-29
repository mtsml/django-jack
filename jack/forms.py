from django import forms
import urllib3

from .models import Channel

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
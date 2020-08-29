from django import forms

from .models import Channel

class ChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ('channel_id', 'channel_nm')
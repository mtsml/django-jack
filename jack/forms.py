from django import forms
import urllib3

from .models import Channel, Comment, Video


VIDEO_URL_PREFIX = 'https://www.youtube.com/watch?v='


def get_video_id_from_url(url):
    return url.replace(VIDEO_URL_PREFIX, '')


class VideoForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'動画URL'
    }))

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


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={
        'placeholder':'コメント'
    }))


class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder':'チャンネル名'
    }))
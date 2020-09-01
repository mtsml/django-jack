from django import forms

from .models import Channel, Comment, Video


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={
        'placeholder': 'コメント'
    }))


class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': '検索ワード'
    }))
import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, SearchForm
from .models import Channel, Comment, Video
from .youtube import search_youtube


def index(request):
    channel_list = Channel.objects.all()
    video_list = Video.objects.all()
    search_form = SearchForm()

    context = {
        'channel_list': channel_list,
        'search_form': search_form,
        'video_list': video_list
    }

    return render(request, 'jack/index.html', context)


def search(request):
    channel_list = []
    video_list = []

    if request.method == 'POST':
        if 'add_channel' in request.POST:
            channel_id = request.POST['channel_id']
            channel_nm = request.POST['channel_nm']
            if not Channel.is_channel_id_exists(channel_id):
                channel = Channel.objects.create(channel_id=channel_id, channel_nm=channel_nm)
        elif 'add_video' in request.POST:
            video_id = request.POST['video_id']
            channel_id = request.POST['channel_id']
            if not Video.is_video_id_exists(video_id):
                channel.video_set.create(video_id=video_id)
        elif 'search' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_result = search_youtube(query)
                channel_list = search_result["channel_list"]
                video_list = search_result["video_list"]

    search_form = SearchForm()

    context = {
        'channel_list': channel_list,
        'search_form': search_form,
        'video_list': video_list
    }

    return render(request, 'jack/search.html', context)


def channel(request, channel_id):
    channel = get_object_or_404(Channel, channel_id=channel_id)

    if request.method == 'POST':
        if 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.create(
                    category='channel', 
                    foreign_id=channel_id,
                    comment=form.cleaned_data['comment'],
                    reg_datetime=datetime.datetime.now()
                )
                return redirect('channel', channel_id=channel_id)

    comment_form = CommentForm()
    search_form = SearchForm()
    video_list = channel.video_set.all()

    context = {
        'channel': channel, 
        'comment_form': comment_form,
        'search_form': search_form,
        'video_list': video_list
    }

    return render(request, 'jack/channel.html', context)


def video(request, video_id):
    message=None
    search_result=[]

    video = get_object_or_404(Video, video_id=video_id)

    if request.method == 'POST':
        if 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.create(
                    category='video', 
                    foreign_id=video_id,
                    comment=form.cleaned_data['comment'],
                    reg_datetime=datetime.datetime.now()
                )
                return redirect('video', video_id=video_id)

    comment_form = CommentForm()
    search_form = SearchForm()

    context = {
        'video': video ,
        'comment_form': comment_form,
        'search_form': search_form
    }

    return render(request, 'jack/video.html', context)
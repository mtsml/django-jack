import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import CommentForm, SearchForm
from .models import Channel, Comment, Video
from .youtube import search_youtube


def index(request):
    channel_list = Channel.objects.all()
    new_video_list = Video.get_new_video_list(5, None)
    popular_video_list = Video.get_popular_video_list(5, None)
    search_form = SearchForm()

    context = {
        'channel_list': channel_list,
        'search_form': search_form,
        'new_video_list': new_video_list,
        'popular_video_list': popular_video_list
    }

    return render(request, 'jack/index.html', context)


def search(request):
    channel_list = []
    video_list = []

    if request.method == 'POST':
        if 'add_channel' in request.POST:
            channel_id = request.POST['channel_id']
            channel_nm = request.POST['channel_nm']
            thumbnails_url = request.POST['thumbnails_url']
            if not Channel.is_channel_id_exists(channel_id):
                channel = Channel.objects.create(
                    channel_id=channel_id, 
                    channel_nm=channel_nm,
                    thumbnails_url=thumbnails_url,
                    reg_datetime=datetime.datetime.now()
                )
            return JsonResponse({})

        elif 'add_video' in request.POST:
            video_id = request.POST['video_id']
            channel_id = request.POST['channel_id']
            video_nm = request.POST['video_nm']
            thumbnails_url = request.POST['thumbnails_url']
            channel = get_object_or_404(Channel, channel_id=channel_id)
            if not Video.is_video_id_exists(video_id):
                channel.video_set.create(
                    video_id=video_id,
                    video_nm=video_nm,
                    thumbnails_url=thumbnails_url,
                    reg_datetime=datetime.datetime.now()
                )
            return JsonResponse({})

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
                comment_text = form.cleaned_data['comment']
                comment = Comment.objects.create(
                    category='channel', 
                    foreign_id=channel_id,
                    comment=comment_text,
                    reg_datetime=datetime.datetime.now()
                )
                comment_form = CommentForm()
                comment_list = channel.get_comment_list()
                context = {
                    'category': 'channel',
                    'foreign_id': channel_id,
                    'comment_form': comment_form,
                    'comment_list': comment_list
                }
                if request.is_ajax():
                    html = render_to_string('jack/component/comment_list.html', context, request=request)
                    return JsonResponse({'form': html}) 

    channel_list = Channel.objects.all()
    comment_form = CommentForm()
    new_video_list = Video.get_new_video_list(5, channel_id)
    popular_video_list = Video.get_popular_video_list(5, channel_id)
    search_form = SearchForm()

    context = {
        'channel': channel, 
        'channel_list': channel_list,
        'comment_form': comment_form,
        'new_video_list': new_video_list,
        'popular_video_list': popular_video_list,
        'search_form': search_form,
    }

    return render(request, 'jack/channel.html', context)


def video(request, video_id):
    video = get_object_or_404(Video, video_id=video_id)

    if request.method == 'POST':
        if 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment_text = form.cleaned_data['comment']
                comment = Comment.objects.create(
                    category='video', 
                    foreign_id=video_id,
                    comment=comment_text,
                    reg_datetime=datetime.datetime.now()
                )
                comment_form = CommentForm()
                comment_list = video.get_comment_list()
                context = {
                    'category': 'video',
                    'foreign_id': video_id,
                    'comment_form': comment_form,
                    'comment_list': comment_list
                }
                if request.is_ajax():
                    html = render_to_string('jack/component/comment_list.html', context, request=request)
                    return JsonResponse({'form': html}) 

    channel_list = Channel.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm()

    context = {
        'channel_list': channel_list,
        'comment_form': comment_form,
        'search_form': search_form,
        'video': video
    }

    return render(request, 'jack/video.html', context)
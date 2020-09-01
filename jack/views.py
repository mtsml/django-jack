import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, SearchForm
from .models import Channel, Comment, Video
from .youtube import search_channel, search_video_in_channel


def index(request):
    message=None
    search_result=[]

    if request.method == 'POST':
        if 'add_channel' in request.POST:            
            channel_id = request.POST['channel_id']
            channel_nm = request.POST['channel_nm']
            if not Channel.is_channel_id_exists(channel_id):
                channel = Channel.objects.create(channel_id=channel_id, channel_nm=channel_nm)
        elif 'search_channel' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_result = search_channel(query)

    channel_list = Channel.objects.all()
    search_form = SearchForm()

    context = {
        'channel_list': channel_list, 
        'message': message,
        'search_form': search_form,
        'search_result': search_result
    }

    return render(request, 'jack/index.html', context)


def detail(request, channel_id):
    message=None
    search_result=[]

    channel = get_object_or_404(Channel, channel_id=channel_id)

    if request.method == 'POST':
        if 'add_video' in request.POST:
            video_id = request.POST['video_id']
            if not Video.is_video_id_exists(video_id):
                channel.video_set.create(video_id=video_id)
        elif 'search_video' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_result = search_video_in_channel(channel_id, query)
        elif 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                video_id = request.POST['video_id']
                comment = Comment.objects.create(
                    category='video', 
                    foreign_id=video_id,
                    comment=form.cleaned_data['comment'],
                    reg_datetime=datetime.datetime.now()
                )
                return redirect('detail', channel_id=channel_id)

    comment_form = CommentForm()
    search_form = SearchForm()
    video_list = channel.video_set.all()

    context = {
        'channel': channel, 
        'comment_form': comment_form,
        'message': message,
        'search_form': search_form,
        'search_result': search_result,
        'video_list': video_list
    }

    return render(request, 'jack/detail.html', context)
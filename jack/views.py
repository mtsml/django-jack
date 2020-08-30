import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Channel, Comment, Video
from .forms import ChannelForm, CommentForm, VideoForm, get_video_id_from_url


MSG_INVALID_CHANNEL_ID = 'そのチャンネルIDは存在しません'
MSG_INVALID_VIDEO_URL = 'そのURLは存在しません'


def index(request):
    message=None # TODO:messageの処理はもっといい方法があるはず
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            message = MSG_INVALID_CHANNEL_ID
    form = ChannelForm()
    channel_list = Channel.objects.all()
    context = {'form': form, 'channel_list': channel_list, 'message': message}    
    return render(request, 'jack/index.html', context)


def detail(request, channel_id):
    message=None # TODO:messageの処理はもっといい方法があるはず
    channel = get_object_or_404(Channel, channel_id=channel_id)
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video_id = get_video_id_from_url(form.cleaned_data['url'])
            channel.video_set.create(video_id=video_id)
            return redirect('detail', channel_id=channel_id)
        else:
            message = MSG_INVALID_VIDEO_URL
    video_form = VideoForm()
    comment_form = CommentForm()
    video_list = channel.video_set.all()
    context = {
        'video_form': video_form, 
        'comment_form': comment_form,
        'channel': channel, 
        'video_list': video_list, 
        'message': message
    }
    return render(request, 'jack/detail.html', context)


def comment(request, category, foreign_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                category=category, 
                foreign_id=foreign_id,
                comment=form.cleaned_data['comment'],
                reg_datetime=datetime.datetime.now()
            )
            if category == 'channel':
                return redirect('detail', channel_id=foreign_id)
            else:
                channel_id = Video.objects.get(video_id=foreign_id).channel_id
                return redirect('detail', channel_id=channel_id)
    return redirect('index') # TODO:エラーページとかに飛ばす
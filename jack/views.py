from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Channel, Video
from .forms import ChannelForm, VideoForm, get_video_id_from_url


def index(request):
    message=None # TODO:messageの処理はもっといい方法があるはず
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            message = 'そのチャンネルIDは存在しません'
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
            message = 'そのURLは存在しません'
    form = VideoForm()
    video_list = channel.video_set.all()
    context = {'form': form, 'channel': channel, 'video_list': video_list, 'message': message}
    return render(request, 'jack/detail.html', context)
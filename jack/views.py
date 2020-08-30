from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Channel, Video
from .forms import ChannelForm


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
    channel = get_object_or_404(Channel, channel_id=channel_id)
    video_list = channel.video_set.all()
    context = {'channel': channel, 'video_list': video_list}
    return render(request, 'jack/detail.html', context)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Channel
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
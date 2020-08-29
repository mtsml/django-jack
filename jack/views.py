from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Channel
from .forms import ChannelForm

def index(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        form = ChannelForm()
    channel_list = Channel.objects.all()
    context = {'form': form, 'channel_list': channel_list}    
    return render(request, 'jack/index.html', context)
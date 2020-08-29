from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Channel


def index(request):
    channel_list = Channel.objects.all()
    context = {'channel_list': channel_list}
    return render(request, 'jack/index.html', context)


def add_channel(request):
    channel_id = request.POST['channel_id']
    channel_nm = request.POST['channel_nm']
    channel = Channel(channel_id=channel_id, channel_nm=channel_nm)
    channel.save()
    return HttpResponseRedirect(reverse('index'))
from django.shortcuts import render

from .models import Channel


def index(request):
    channel_list = Channel.objects.all()
    context = {'channel_list': channel_list}
    return render(request, 'jack/index.html', context)
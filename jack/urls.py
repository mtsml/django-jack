from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('channel/<str:channel_id>/', views.channel, name='channel'),
    path('video/<str:video_id>/', views.video, name='video')
]
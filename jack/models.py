from django.db import models


class Channel(models.Model):
    channel_id = models.CharField(max_length=200) # TODO:チャンネルIDの最大文字数を調べる
    channel_nm = models.CharField(max_length=200)

    def __str__(self):
        return self.channel_id


class Video(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=200)

    def __str__(self):
        return self.video_id
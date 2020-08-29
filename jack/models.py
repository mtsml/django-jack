from django.db import models

# Create your models here.
class Channel(models.Model):
    channel_id = models.CharField(max_length=200) # TODO:チャンネルIDの最大文字数を調べる
    channel_nm = models.CharField(max_length=200)

    def __str__(self):
        return self.channel_id
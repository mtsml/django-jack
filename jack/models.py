from django.db import models


class Channel(models.Model):
    channel_id = models.CharField(max_length=200) # TODO:チャンネルIDの最大文字数を調べる
    channel_nm = models.CharField(max_length=200)

    def __str__(self):
        return self.channel_id
    
    def is_channel_id_exists(channel_id):
        return Channel.objects.filter(channel_id=channel_id).exists()

    def get_comment_list(self):
        return Comment.objects.filter(category='channel', foreign_id=self.channel_id).order_by('-reg_datetime')


class Video(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=200)

    def __str__(self):
        return self.video_id

    def get_comment_list(self):
        return Comment.objects.filter(category='video', foreign_id=self.video_id).order_by('-reg_datetime')


class Comment(models.Model):
    category = models.CharField(max_length=200)
    foreign_id = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)
    reg_datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.category}:{self.foreign_id}'
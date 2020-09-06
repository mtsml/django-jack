from django.db import models


class Channel(models.Model):
    channel_id = models.CharField(max_length=200) # TODO:チャンネルIDの最大文字数を調べる
    channel_nm = models.CharField(max_length=200)
    thumbnails_url = models.CharField(max_length=3000, null=True)
    reg_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.channel_id
    
    def is_channel_id_exists(channel_id):
        return Channel.objects.filter(channel_id=channel_id).exists()

    def get_comment_list(self):
        return Comment.objects.filter(category='channel', foreign_id=self.channel_id).order_by('-reg_datetime')


class Video(models.Model):
    video_id = models.CharField(max_length=200)
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_nm = models.CharField(max_length=200)
    thumbnails_url = models.CharField(max_length=3000, null=True)
    reg_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.video_id

    def is_video_id_exists(video_id):
        return Video.objects.filter(video_id=video_id).exists()

    def get_new_video_list(cnt):
        return Video.objects.order_by('-reg_datetime').all()[:cnt]

    def get_popular_video_list(cnt):
        # TODO: パフォーマンスのボトルネック
        video_list = Video.objects.raw(f"""
            SELECT
                id
        	    ,video_id
	            ,channel_id_id
                ,video_nm
                ,thumbnails_url
	            ,(SELECT COUNT(*) FROM jack_comment WHERE category = 'video' AND foreign_id = video_id) AS cnt
            FROM jack_video
            ORDER BY cnt DESC
            LIMIT {cnt};""")
        return video_list

    def get_comment_list(self):
        return Comment.objects.filter(category='video', foreign_id=self.video_id).order_by('-reg_datetime')


class Comment(models.Model):
    category = models.CharField(max_length=200)
    foreign_id = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)
    reg_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.category}:{self.foreign_id}'
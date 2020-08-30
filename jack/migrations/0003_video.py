# Generated by Django 3.1 on 2020-08-30 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jack', '0002_remove_channel_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=200)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jack.channel')),
            ],
        ),
    ]

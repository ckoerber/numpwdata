# Generated by Django 3.1.5 on 2021-01-14 09:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='The title of the notification', max_length=200, null=True)),
                ('content', models.TextField(help_text='The content of the notification')),
                ('level', models.CharField(choices=[('DEBUG', 'DEBUG'), ('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR')], help_text='The level of the notification mimicing logging levels', max_length=8)),
                ('tag', models.CharField(blank=True, help_text='A tag for fast searches', max_length=100, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Creation date of the notification')),
                ('groups', models.ManyToManyField(blank=True, help_text='The group of users who are allowed to read this notification', related_name='notifications', to='auth.Group')),
                ('read_by', models.ManyToManyField(blank=True, help_text='The users who have read the notification', related_name='read_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
# Generated by Django 3.1.5 on 2021-01-14 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0004_auto_20210114_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operator2npwd',
            name='qvals',
        ),
    ]

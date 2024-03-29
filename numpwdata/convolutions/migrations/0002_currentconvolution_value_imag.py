# Generated by Django 3.2.4 on 2021-06-22 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convolutions', '0001_squashed_0003_auto_20210114_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentconvolution',
            name='value_imag',
            field=models.FloatField(blank=True, help_text='Imaginary value of the matrix element.', null=True),
        ),
    ]

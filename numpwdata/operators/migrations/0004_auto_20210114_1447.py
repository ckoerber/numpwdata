# Generated by Django 3.1.5 on 2021-01-14 14:47

from django.db import migrations, models
import numpwdata.utils.encoders


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0003_auto_20210114_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operator2npwd',
            name='l12_max',
        ),
        migrations.RemoveField(
            model_name='operator2npwd',
            name='s12_max',
        ),
        migrations.AlterField(
            model_name='operator2npwd',
            name='args',
            field=models.JSONField(blank=True, encoder=numpwdata.utils.encoders.NympyEncoder, help_text='Information about the operator arguments', null=True),
        ),
        migrations.AlterField(
            model_name='operator2npwd',
            name='qvals',
            field=models.JSONField(blank=True, encoder=numpwdata.utils.encoders.NympyEncoder, help_text='Information about the external current momentum exchange range.', null=True),
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-14 11:19

from django.db import migrations, models
import numpwdata.utils.encoders


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0002_auto_20210114_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator1n',
            name='legend',
            field=models.JSONField(blank=True, encoder=numpwdata.utils.encoders.NympyEncoder, help_text='A dictinoary explaining the definitions.', null=True),
        ),
        migrations.AlterField(
            model_name='operator2n',
            name='legend',
            field=models.JSONField(blank=True, encoder=numpwdata.utils.encoders.NympyEncoder, help_text='A dictinoary explaining the definitions.', null=True),
        ),
        migrations.AlterField(
            model_name='operator2npwd',
            name='args',
            field=models.JSONField(encoder=numpwdata.utils.encoders.NympyEncoder, help_text='Information about the operator arguments'),
        ),
        migrations.AlterField(
            model_name='operator2npwd',
            name='misc',
            field=models.JSONField(blank=True, encoder=numpwdata.utils.encoders.NympyEncoder, help_text='Miscellaneous information about the operator like quantum channels.', null=True),
        ),
        migrations.AlterField(
            model_name='operator2npwd',
            name='qvals',
            field=models.JSONField(encoder=numpwdata.utils.encoders.NympyEncoder, help_text='Information about the external current momentum exchange range.'),
        ),
    ]

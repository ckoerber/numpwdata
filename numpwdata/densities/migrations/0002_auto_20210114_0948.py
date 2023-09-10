# Generated by Django 3.1.5 on 2021-01-14 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_datfile'),
        ('densities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='density1n',
            name='file',
            field=models.OneToOneField(help_text='File information about density.', on_delete=django.db.models.deletion.CASCADE, to='files.datfile'),
        ),
        migrations.AlterField(
            model_name='density2n',
            name='file',
            field=models.OneToOneField(help_text='File information about density.', on_delete=django.db.models.deletion.CASCADE, to='files.h5file'),
        ),
    ]
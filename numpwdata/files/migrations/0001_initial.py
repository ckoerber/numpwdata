# Generated by Django 3.1.5 on 2021-01-14 09:17

import _socket
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='H5File',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='files.file')),
                ('path', models.TextField(help_text='File path address to the HDF5 file.')),
                ('h5_path', models.TextField(default='/', help_text='Group path address within the HDF5 file.')),
                ('hostname', models.TextField(default=_socket.gethostname, help_text='Name of the (remote) host of the file.')),
            ],
            options={
                'unique_together': {('path', 'h5_path', 'hostname')},
            },
            bases=('files.file',),
        ),
    ]

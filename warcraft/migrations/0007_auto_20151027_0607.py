# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import simple_email_confirmation.models


class Migration(migrations.Migration):

    dependencies = [
        ('warcraft', '0006_auto_20151022_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('web', models.BooleanField(default=False)),
                ('internal', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('userName', models.CharField(unique=True, max_length=31)),
                ('picture', models.ImageField(upload_to=b'images')),
                ('firstName', models.CharField(max_length=31)),
                ('lastName', models.CharField(max_length=31)),
                ('email', models.EmailField(max_length=254, verbose_name=b'email address')),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('login_internal', models.BooleanField(default=False)),
                ('login_web', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(simple_email_confirmation.models.SimpleEmailConfirmationUserMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='loggeduser',
            name='user',
            field=models.ForeignKey(to='warcraft.User'),
        ),
    ]

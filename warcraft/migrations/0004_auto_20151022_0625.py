# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('warcraft', '0003_auto_20151020_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=datetime.datetime(2015, 10, 22, 6, 25, 21, 977700, tzinfo=utc), upload_to=b'images'),
            preserve_default=False,
        ),
    ]

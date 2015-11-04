# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warcraft', '0007_auto_20151027_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emailEvery',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warcraft', '0005_auto_20151022_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='loss',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wins',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

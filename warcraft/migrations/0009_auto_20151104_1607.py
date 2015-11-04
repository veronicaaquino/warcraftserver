# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warcraft', '0008_user_emailevery'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='losses',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ranking',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.FloatField(default=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='wins',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

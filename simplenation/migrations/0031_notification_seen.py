# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0030_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]

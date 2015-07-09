# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0031_notification_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='humanized_created_at',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]

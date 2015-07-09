# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0010_auto_20150104_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='definition',
            name='post_date',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0005_auto_20141230_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]

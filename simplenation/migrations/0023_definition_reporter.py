# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0022_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='reporter',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

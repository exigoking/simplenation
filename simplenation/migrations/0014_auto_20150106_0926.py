# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0013_definition_last_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='last_posted',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]

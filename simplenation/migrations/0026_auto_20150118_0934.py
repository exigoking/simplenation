# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0025_auto_20150118_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='score',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0019_term_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='account_deletion_key',
            field=models.CharField(default='deletion_key_defualt', max_length=64, blank=True),
            preserve_default=False,
        ),
    ]

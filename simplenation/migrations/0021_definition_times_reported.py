# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0020_author_account_deletion_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='times_reported',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

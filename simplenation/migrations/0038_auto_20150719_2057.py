# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0037_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='to_add',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='picture',
            name='to_delete',
            field=models.BooleanField(default=False),
        ),
    ]

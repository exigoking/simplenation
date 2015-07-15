# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0033_auto_20150708_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='author',
            field=models.ForeignKey(to='simplenation.Author', null=True),
        ),
    ]

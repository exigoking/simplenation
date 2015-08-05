# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0038_auto_20150719_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='author',
            field=models.ForeignKey(to='simplenation.Author', null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='term',
            field=models.ForeignKey(to='simplenation.Term', null=True),
        ),
    ]

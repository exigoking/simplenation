# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0035_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='term',
            field=models.ForeignKey(related_name='pictures_for_term', to='simplenation.Term', null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='definition',
            field=models.ForeignKey(related_name='pictures_for_explanation', to='simplenation.Definition'),
        ),
    ]

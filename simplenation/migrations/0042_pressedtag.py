# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0041_term_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='PressedTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('session', models.ForeignKey(related_name='pressed_tags', to='simplenation.Session')),
            ],
        ),
    ]

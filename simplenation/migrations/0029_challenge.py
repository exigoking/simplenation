# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simplenation', '0028_favourite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('challengee', models.ForeignKey(related_name='challengees', verbose_name='challengee', to=settings.AUTH_USER_MODEL)),
                ('challenger', models.ForeignKey(related_name='challengers', verbose_name='challenger', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(related_name='terms', verbose_name='subject', to='simplenation.Term')),
            ],
        ),
    ]

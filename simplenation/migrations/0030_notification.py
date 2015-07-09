# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simplenation', '0029_challenge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typeof', models.CharField(default=b'', max_length=140, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('definition', models.ForeignKey(related_name='event_notifications', to='simplenation.Definition', null=True)),
                ('receiver', models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sent_notifications', to=settings.AUTH_USER_MODEL)),
                ('term', models.ForeignKey(related_name='term_notifications', to='simplenation.Term', null=True)),
            ],
        ),
    ]

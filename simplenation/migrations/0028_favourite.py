# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simplenation', '0027_author_num_of_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('favoree', models.ForeignKey(related_name='favorees', verbose_name='favoree', to=settings.AUTH_USER_MODEL)),
                ('favoror', models.ForeignKey(related_name='_unused_', verbose_name='favoror', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

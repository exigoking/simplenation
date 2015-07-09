# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippets', '0002_auto_20150224_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default=b'', max_length=100, blank=True)),
                ('code', models.TextField()),
                ('linenos', models.BooleanField(default=False)),
                ('language', models.CharField(default=b'python', max_length=100)),
                ('style', models.CharField(default=b'friendly', max_length=100)),
                ('highlighted', models.TextField(blank=True)),
                ('owner', models.ForeignKey(related_name='snippets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
    ]

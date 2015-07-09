# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simplenation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.CharField(max_length=1024)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=512)),
                ('likes', models.IntegerField(default=0)),
                ('post_date', models.DateField()),
                ('author', models.ForeignKey(to='simplenation.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Terms',
            new_name='Term',
        ),
        migrations.RemoveField(
            model_name='authors',
            name='user',
        ),
        migrations.RemoveField(
            model_name='definitions',
            name='author',
        ),
        migrations.DeleteModel(
            name='Authors',
        ),
        migrations.RemoveField(
            model_name='definitions',
            name='term',
        ),
        migrations.DeleteModel(
            name='Definitions',
        ),
        migrations.AddField(
            model_name='definition',
            name='term',
            field=models.ForeignKey(to='simplenation.Term'),
            preserve_default=True,
        ),
    ]

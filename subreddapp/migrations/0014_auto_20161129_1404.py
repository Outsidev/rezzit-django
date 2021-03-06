# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subreddapp', '0013_auto_20161129_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='subreddapp.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_mainposts', to='subreddapp.UserProfile'),
        ),
    ]

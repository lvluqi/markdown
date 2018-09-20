# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-13 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('publish', models.CharField(max_length=32)),
                ('pub_date', models.DateTimeField()),
            ],
        ),
    ]

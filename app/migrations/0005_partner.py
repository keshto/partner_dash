# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_appuser_avatar512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('logo', models.CharField(max_length=500)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_partner', to='app.Card')),
            ],
        ),
    ]

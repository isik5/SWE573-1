# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search_entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usda.Food')),
            ],
        ),
        migrations.CreateModel(
            name='Search_query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_string', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='search_entry',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usda.Search_query'),
        ),
    ]
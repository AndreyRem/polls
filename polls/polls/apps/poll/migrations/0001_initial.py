# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 17:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Ответ')),
                ('selection_count', models.IntegerField(default=0, verbose_name='Количество выборов данного ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.CharField(max_length=200, null=True, verbose_name='Адрес')),
                ('weight', models.FloatField(default=0, verbose_name='Вес опроса')),
                ('successful_completion_count', models.IntegerField(default=0, verbose_name='Количество успешных прохождений')),
                ('not_successful_completion_count', models.IntegerField(default=0, verbose_name='Количество не полных прохождений')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
                'ordering': ('-weight', '-successful_completion_count'),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('respondents_count', models.IntegerField(default=0, verbose_name='Количество респондентов')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Poll')),
            ],
            options={
                'verbose_name': 'Вопрос опроса',
                'verbose_name_plural': 'Вопросы опросов',
                'ordering': ('poll',),
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question'),
        ),
    ]

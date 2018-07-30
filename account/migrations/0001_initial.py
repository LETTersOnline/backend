# Generated by Django 2.0.7 on 2018-07-30 09:21

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('date_active', models.DateTimeField(auto_now=True)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(5, 'SUPER_ADMIN'), (4, 'ADMIN'), (3, 'COACH'), (2, 'LETTERS'), (1, 'REGULAR')], default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('uid', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('fullname', models.CharField(default='佚名', max_length=128)),
                ('school', models.CharField(blank=True, max_length=200, null=True)),
                ('major', models.CharField(blank=True, max_length=200, null=True)),
                ('mood', models.TextField(null=True)),
                ('accepted_number', models.IntegerField(default=0)),
                ('total_score', models.BigIntegerField(default=0)),
                ('submission_number', models.IntegerField(default=0)),
                ('extends', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

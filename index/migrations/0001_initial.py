# Generated by Django 2.2.5 on 2019-12-23 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('body', models.TextField()),
                ('tag', models.CharField(max_length=20)),
                ('post_time', models.CharField(default=datetime.datetime(2019, 12, 23, 11, 17, 13, 59255), max_length=50)),
                ('author', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Blogs',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=30)),
                ('token', models.CharField(blank=True, max_length=64)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-22 03:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.BigIntegerField(blank=True, default=None, null=True)),
                ('mbid', models.CharField(max_length=36)),
                ('title', models.CharField(max_length=300)),
                ('status', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mbid', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, choices=[('Person', 'Individual person'), ('Group', 'Band or group of people'), ('Orchestra', 'Orchestra or large instrumental ensemble'), ('Choir', 'Choir or large vocal ensemble'), ('Character', 'Fictional character'), ('Other', 'Other'), ('', 'None')], default='', max_length=9)),
                ('disambiguation', models.CharField(blank=True, default='', max_length=100)),
                ('ended', models.NullBooleanField()),
                ('albums', models.ManyToManyField(to='app.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('subregion', models.CharField(max_length=70)),
                ('population', models.PositiveIntegerField()),
                ('alpha2code', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utc_offset', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mbid', models.CharField(max_length=36)),
                ('title', models.CharField(max_length=50)),
                ('length', models.IntegerField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Artist')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='languages',
            field=models.ManyToManyField(to='app.Language'),
        ),
        migrations.AddField(
            model_name='country',
            name='timezones',
            field=models.ManyToManyField(to='app.TimeZone'),
        ),
        migrations.AddField(
            model_name='artist',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Country'),
        ),
        migrations.AddField(
            model_name='album',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Country'),
        ),
    ]

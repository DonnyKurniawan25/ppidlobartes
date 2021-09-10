# Generated by Django 3.2.6 on 2021-09-03 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppid', '0009_auto_20210902_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='download',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_download', to='ppid.IpModel'),
        ),
        migrations.AlterField(
            model_name='data',
            name='read',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_views', to='ppid.IpModel'),
        ),
    ]
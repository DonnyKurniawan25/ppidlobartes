# Generated by Django 3.2.6 on 2021-09-06 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppid', '0015_layanan_type_layanan'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinas',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='dinas',
            name='telp',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='dinas',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.2.6 on 2021-08-31 01:02

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
            name='IpModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Type_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Type_pemohon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_pemohon', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Form_information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('telp', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=50)),
                ('ktp', models.FileField(upload_to='')),
                ('purpose', models.TextField()),
                ('detail', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=125)),
                ('Information', models.TextField()),
                ('kategory_pemohon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppid.type_pemohon')),
            ],
        ),
        migrations.CreateModel(
            name='Dinas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('shortness', models.CharField(max_length=50)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dinas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=125)),
                ('title', models.CharField(max_length=225)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, null=True, unique=True)),
                ('responsible', models.CharField(max_length=225)),
                ('information', models.CharField(max_length=225)),
                ('date', models.DateField(auto_now_add=True)),
                ('date_a', models.DateField()),
                ('date_b', models.DateField()),
                ('file', models.FileField(upload_to='')),
                ('size', models.CharField(blank=True, max_length=225, null=True)),
                ('dinas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ppid.dinas')),
                ('download', models.ManyToManyField(blank=True, null=True, related_name='post_download', to='ppid.IpModel')),
                ('read', models.ManyToManyField(blank=True, null=True, related_name='post_views', to='ppid.IpModel')),
                ('type_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppid.type_data')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
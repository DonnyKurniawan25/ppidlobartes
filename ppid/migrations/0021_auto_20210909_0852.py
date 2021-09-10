# Generated by Django 3.2.6 on 2021-09-09 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ppid', '0020_alter_dinas_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinas',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dinas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='form_information',
            name='status',
            field=models.CharField(blank=True, choices=[('Belum Diproses', 'Belum Diproses'), ('Diberikan', 'Diberikan'), ('Ditolak', 'Ditolak')], max_length=125, null=True),
        ),
    ]
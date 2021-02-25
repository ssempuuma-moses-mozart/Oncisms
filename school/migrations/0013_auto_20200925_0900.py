# Generated by Django 3.0.6 on 2020-09-25 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_auto_20200824_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterandenergysource',
            name='energy_sources',
        ),
        migrations.RemoveField(
            model_name='waterandenergysource',
            name='water_sources',
        ),
        migrations.AddField(
            model_name='waterandenergysource',
            name='energy_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.EnergySource'),
        ),
        migrations.AddField(
            model_name='waterandenergysource',
            name='water_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.WaterSource'),
        ),
    ]

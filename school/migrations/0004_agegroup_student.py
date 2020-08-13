# Generated by Django 3.0.6 on 2020-08-13 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ministry', '0013_auto_20200810_1008'),
        ('school', '0003_delete_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('girls', models.IntegerField(blank=True)),
                ('boys', models.IntegerField(blank=True)),
                ('year', models.IntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('age', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.AgeGroup')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ministry.Class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'class_name', 'age', 'year')},
            },
        ),
    ]

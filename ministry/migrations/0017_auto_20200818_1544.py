# Generated by Django 3.0.6 on 2020-08-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0016_auto_20200818_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='date_registered',
        ),
        migrations.AddField(
            model_name='teacher',
            name='on_payroll',
            field=models.BooleanField(default=True),
        ),
    ]

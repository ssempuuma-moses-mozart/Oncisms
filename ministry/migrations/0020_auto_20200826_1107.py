# Generated by Django 3.0.6 on 2020-08-26 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0019_auto_20200820_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parish',
            name='parish_name',
            field=models.CharField(max_length=45, verbose_name='Parish'),
        ),
    ]
# Generated by Django 3.2.9 on 2021-11-22 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCenso', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vivienda',
            name='area',
            field=models.IntegerField(default=0),
        ),
    ]

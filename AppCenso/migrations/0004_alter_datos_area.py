# Generated by Django 3.2.9 on 2021-11-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCenso', '0003_alter_datos_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos',
            name='area',
            field=models.IntegerField(default=0),
        ),
    ]
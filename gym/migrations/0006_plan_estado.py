# Generated by Django 4.2 on 2023-07-09 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0005_rename_idplanpersona_marcacion_plan_persona'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='estado',
            field=models.CharField(default='activo', max_length=10),
        ),
    ]

# Generated by Django 4.2 on 2023-09-05 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0011_alter_estados_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpersona',
            name='estado',
            field=models.CharField(max_length=10),
        ),
    ]
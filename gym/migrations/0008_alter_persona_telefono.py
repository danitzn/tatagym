# Generated by Django 4.2 on 2023-07-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0007_remove_plan_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='telefono',
            field=models.CharField(max_length=30),
        ),
    ]

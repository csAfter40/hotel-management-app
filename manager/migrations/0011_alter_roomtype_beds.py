# Generated by Django 4.0.1 on 2022-02-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_roomtype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='beds',
            field=models.JSONField(null=True),
        ),
    ]
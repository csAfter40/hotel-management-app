# Generated by Django 4.0.1 on 2022-02-10 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_floor_hotel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='owner',
            new_name='owners',
        ),
    ]

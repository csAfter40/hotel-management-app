# Generated by Django 4.0.1 on 2022-02-23 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_rename_room_name_room_name_room_sort_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('name', 'floor'), ('sort_id', 'floor')},
        ),
    ]
# Generated by Django 4.0.1 on 2022-02-23 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_alter_room_cleaning_status_alter_room_vacancy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='room',
            name='sort_id',
            field=models.SmallIntegerField(default=1, null=True),
        ),
    ]

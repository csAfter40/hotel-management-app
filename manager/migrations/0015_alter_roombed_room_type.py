# Generated by Django 4.0.1 on 2022-02-18 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_alter_roombed_room_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roombed',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_beds', to='manager.roomtype'),
        ),
    ]

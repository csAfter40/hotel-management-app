# Generated by Django 4.0.1 on 2022-02-18 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_rename_vacansy_room_vacancy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roombed',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_types', to='manager.roomtype'),
        ),
    ]

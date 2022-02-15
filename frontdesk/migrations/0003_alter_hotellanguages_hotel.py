# Generated by Django 4.0.1 on 2022-01-27 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
        ('frontdesk', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotellanguages',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='manager.hotel'),
        ),
    ]
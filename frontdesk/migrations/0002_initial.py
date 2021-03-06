# Generated by Django 4.0.1 on 2022-01-27 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_currency_language_country'),
        ('frontdesk', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_types', to='manager.hotel'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='guest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontdesk.guest'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.hotel'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontdesk.roomtype'),
        ),
        migrations.AddField(
            model_name='hotellanguages',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.hotel'),
        ),
        migrations.AddField(
            model_name='guest',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontdesk.hotellanguages'),
        ),
        migrations.AddField(
            model_name='guest',
            name='nationality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.country'),
        ),
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='folio',
            name='reservation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='folio', to='frontdesk.reservation'),
        ),
        migrations.AddField(
            model_name='expense',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.currency'),
        ),
        migrations.AddField(
            model_name='expense',
            name='folio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='frontdesk.folio'),
        ),
    ]

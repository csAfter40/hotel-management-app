# Generated by Django 4.0.1 on 2022-01-27 17:17

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
            ],
        ),
        migrations.CreateModel(
            name='Folio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('guest_type', models.CharField(choices=[('FT', 'First Timer'), ('VIP', 'VIP')], max_length=16)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('id_type', models.CharField(choices=[('I', 'Id card'), ('P', 'passport')], max_length=16)),
                ('id_number', models.CharField(max_length=32)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='HotelLanguages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('EN', 'English'), ('RU', 'Russian'), ('DE', 'German')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('RES', 'reserved'), ('CAN', 'cancelled'), ('ARR', 'arrival'), ('CIN', 'checked in'), ('DEP', 'departure'), ('OUT', 'checked out'), ('NOS', 'no show')], default=('RES', 'reserved'), max_length=3)),
                ('arrival_date', models.DateField()),
                ('departure_date', models.DateField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('meal_plan', models.TextField(choices=[('EP', 'Europen Plan'), ('AP', 'American Plan'), ('MAP', 'Modified American Plan'), ('CP', 'Continental Plan')], max_length=3)),
                ('adult_qty', models.PositiveSmallIntegerField()),
                ('child_qty', models.PositiveSmallIntegerField(default=0)),
                ('source', models.CharField(choices=[('WEB', 'website'), ('TEL', 'telephone'), ('BOO', 'booking.com'), ('HOT', 'hotels.com')], max_length=3)),
                ('rate_plan', models.CharField(choices=[('NOR', 'normal'), ('PRO', 'promotion')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True)),
            ],
        ),
    ]
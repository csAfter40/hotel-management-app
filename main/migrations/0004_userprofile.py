# Generated by Django 4.0.1 on 2022-03-11 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_language_symbol_currency_symbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('profile_picture', models.ImageField(default='profile_pictures/default.jpg', upload_to=main.models.upload_to, verbose_name='Profile Picture')),
                ('nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.country')),
            ],
        ),
    ]

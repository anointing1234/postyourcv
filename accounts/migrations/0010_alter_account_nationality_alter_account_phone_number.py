# Generated by Django 5.2 on 2025-04-29 10:39

import django_countries.fields
import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_playerjobapplication_coach_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='nationality',
            field=django_countries.fields.CountryField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, null=True, region=None),
        ),
    ]

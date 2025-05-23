# Generated by Django 5.2 on 2025-04-28 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_birth_date_account_birth_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifiedPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False, help_text='Has this player passed admin verification?')),
                ('is_available', models.BooleanField(default=True, help_text='Is this player currently available for selection?')),
                ('current_activity', models.CharField(blank=True, choices=[('training', 'Training'), ('match', 'Match'), ('rest', 'Rest'), ('rehab', 'Rehab')], help_text='Current football activity/status', max_length=20, null=True)),
                ('notes', models.TextField(blank=True, help_text='Any additional notes (e.g. injury details)')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verified_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verified Player Profile',
                'verbose_name_plural': 'Verified Player Profiles',
                'ordering': ['-added_on'],
            },
        ),
    ]

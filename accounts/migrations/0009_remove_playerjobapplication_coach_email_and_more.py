# Generated by Django 5.2 on 2025-04-29 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_footballjob_apply_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='coach_email',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='coach_phone',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='country',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='current_league',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='current_location',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='dominant_positions',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='height_cm',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='highlight_video_url',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='passport_issuing_country',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='primary_language',
        ),
        migrations.RemoveField(
            model_name='playerjobapplication',
            name='weight_kg',
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='coach_contact',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='accounts.footballjob'),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='player_video_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='position',
            field=models.CharField(blank=True, choices=[('GK', 'Goalkeeper'), ('DF', 'Defender'), ('MF', 'Midfielder'), ('FW', 'Forward')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='preferred_foot',
            field=models.CharField(blank=True, choices=[('Left', 'Left'), ('Right', 'Right'), ('Both', 'Both')], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='previous_clubs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='player_photos/'),
        ),
        migrations.AddField(
            model_name='playerjobapplication',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='playerjobapplication',
            name='coach_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='playerjobapplication',
            name='current_club',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='playerjobapplication',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='playerjobapplication',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='playerjobapplication',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]

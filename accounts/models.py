import json
import locale
import random
import string
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from io import BytesIO
from PIL import Image

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The email address is required")
        if not username:
            raise ValueError("The username is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The email address is required for superusers")
        if not username:
            raise ValueError("The username is required for superusers")
        if not password:
            raise ValueError("The password is required for superusers")

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, username=username, password=password, **extra_fields)


# Football-specific choices
POSITION_CHOICES = [
    ('GK', 'Goalkeeper'),
    ('DF', 'Defender'),
    ('MF', 'Midfielder'),
    ('FW', 'Forward'),
]

FOOT_CHOICES = [
    ('Left', 'Left'),
    ('Right', 'Right'),
    ('Both', 'Both'),
]

class Account(AbstractBaseUser, PermissionsMixin):
    # Login & identity
    username        = models.CharField(max_length=150, unique=True)
    email           = models.EmailField(max_length=254, unique=True)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)

    # Contact & bio
    phone_number    = PhoneNumberField(max_length=20, blank=True, null=True)
    date_of_birth   = models.DateField(blank=True, null=True)
    nationality     = CountryField(max_length=50, blank=True, null=True)
    bio             = models.TextField(blank=True, null=True, help_text="A short personal bio")
    birth_date      = models.CharField(max_length=100,blank=True,null=True, help_text="e.g january 5th, 1996")
    birth_place     = models.CharField(max_length=100,blank=True,null=True ,help_text="e.g Manchester - UK")


    # Football-specific
    height          = models.DecimalField(
                        max_digits=5, decimal_places=2,
                        blank=True, null=True,
                        help_text="Height in cm"
                     )
    weight          = models.DecimalField(
                        max_digits=5, decimal_places=2,
                        blank=True, null=True,
                        help_text="Weight in kg"
                     )
    position        = models.CharField(
                        max_length=2,
                        choices=POSITION_CHOICES,
                        blank=True, null=True
                     )
    preferred_foot  = models.CharField(
                        max_length=5,
                        choices=FOOT_CHOICES,
                        blank=True, null=True
                     )
    profile_image  = models.ImageField(upload_to='profile_pics/',
                        default='profile_pics/profile_pic.webp',
                        blank=True)

    # Meta
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)

    # Permissions
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    # Manager & auth setup
    objects         = AccountManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_picture_url(self):
        return self.profile_image.url if self.profile_image else settings.MEDIA_URL + 'profile_pics/profile_pic.webp' 



ACTIVITY_CHOICES = [
    ('training', 'Training'),
    ('match',    'Match'),
    ('rest',     'Rest'),
    ('rehab',    'Rehab'),
]

class VerifiedPlayer(models.Model):
    """
    A separate model where admins can
    link to an Account and control
    verification, availability, and activities.
    """
    account       = models.OneToOneField(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name='verified_profile'
                    )
    is_verified   = models.BooleanField(
                        default=False,
                        help_text="Has this player passed admin verification?"
                    )
    is_available  = models.BooleanField(
                        default=True,
                        help_text="Is this player currently available for selection?"
                    )
    # Optionally track what they're doing right now:
    current_activity = models.CharField(
                           max_length=20,
                           choices=ACTIVITY_CHOICES,
                           blank=True,
                           null=True,
                           help_text="Current football activity/status"
                       )
    notes         = models.TextField(
                        blank=True,
                        help_text="Any additional notes (e.g. injury details)"
                    )
    added_on      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Verified Player Profile"
        verbose_name_plural = "Verified Player Profiles"
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.account.username} Profile"



POSITION_CHOICES = [
    ('GK', 'Goalkeeper'),
    ('DF', 'Defender'),
    ('MF', 'Midfielder'),
    ('FW', 'Forward'),
]

FOOT_CHOICES = [
    ('Left', 'Left'),
    ('Right', 'Right'),
    ('Both', 'Both'),
]

class FootballJob(models.Model):
    country_name = models.CharField(max_length=100, blank=True, null=True)
    country_flag = models.ImageField(upload_to='country_flags/', blank=True, null=True)
    position_title = models.CharField(max_length=100, blank=True, null=True)
    requirement_description = models.TextField(blank=True, null=True)
    salary_offer = models.CharField(max_length=100, blank=True, null=True)
    age_range = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position_title} in {self.country_name}"






class PlayerJobApplication(models.Model):
    job = models.ForeignKey(FootballJob, on_delete=models.CASCADE, related_name='applications', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications', blank=True, null=True)
    
    # Personal Information
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField()
    nationality = CountryField()
    phone_number = PhoneNumberField()
    email_address = models.EmailField()

    address = models.CharField(max_length=255, blank=True, null=True)
    current_club = models.CharField(max_length=100, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    previous_clubs = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, blank=True, null=True)
    preferred_foot = models.CharField(max_length=5, choices=FOOT_CHOICES, blank=True, null=True)
    coach_name = models.CharField(max_length=100, blank=True, null=True)
    coach_contact = models.CharField(max_length=20, blank=True, null=True)
    player_video_link = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='player_photos/', blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} — applied for {self.job}"

    def approve(self):
        self.status = 'approved'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()








class ResetCode(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("used", "Used"),
        ("expired", "Expired"),
        ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    reset_code = models.CharField(max_length=6, blank=True, null=True)  # 6-digit password reset code
    reset_code_created_at = models.DateTimeField(auto_now=True)
    reset_code_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    
    def __str__(self):
        return f"{self.user.username}'s Reset Codes"

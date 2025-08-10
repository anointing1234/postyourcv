# your_app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.html import format_html

from .models import Account,PlayerJobApplication,VerifiedPlayer,FootballJob,ResetCode


#
# 1) Forms for creating and changing Account
#
class AccountCreationForm(forms.ModelForm):
    """Form for creating new users in the admin with password confirmation."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don’t match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    """Form for updating existing users in the admin, showing a read-only hash."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password',
            'is_active', 'is_staff', 'is_admin', 'is_superuser',
            'groups', 'user_permissions'
        )

    def clean_password(self):
        return self.initial["password"]



@admin.register(Account)
class AccountAdmin(UnfoldModelAdmin, UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = (
        'display_profile_picture', 'username', 'email', 'full_name',
        'is_staff', 'is_admin', 'is_active', 'date_joined'
    )
    list_filter = (
        'is_staff', 'is_admin', 'is_active',
        'position', 'preferred_foot', 'nationality'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    # Used by UserAdmin for "Add User" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2'
            ),
        }),
    )

    # Change‐view fieldsets, collapsible by django-unfold
    fieldsets = (
        ('Login & Identity', {
            'fields': ('username', 'email', 'password'),
        }),
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'date_of_birth',
                'nationality', 'phone_number', 'bio'
            ),
        }),
        ('Football Profile', {
            'fields': (
                'position', 'preferred_foot', 'height',
                'weight', 'profile_image'
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_admin',
                'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # Helper columns
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    # Updated method for displaying the profile image preview
    def profile_thumbnail(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;border-radius:50%; object-fit: cover;" />',
                obj.profile_image.url
            )
        return format_html(
            '<img src="/media/profile_pics/profile_pic.webp" style="height:40px;width:40px;border-radius:50%; object-fit: cover;" />'
        )
    profile_thumbnail.short_description = 'Photo'

    # Add a method to display profile picture in the admin list view
    def display_profile_picture(self, obj):
        return self.profile_thumbnail(obj)
    display_profile_picture.short_description = 'Profile Picture'




@admin.register(VerifiedPlayer)
class VerifiedPlayerAdmin(UnfoldModelAdmin):
    # Columns shown in the changelist
    list_display = (
        'account',
        'is_verified',
        'is_available',
        'current_activity',
        'added_on',
    )
    # Which columns are editable right on the changelist
    list_editable = (
        'is_verified',
        'is_available',
    )
    # Make the account link clickable
    list_display_links = ('account',)

    # Filters in the right sidebar
    list_filter = (
        'is_verified',
        'is_available',
        'current_activity',
    )
    # Quick search
    search_fields = (
        'account__username',
        'account__first_name',
        'account__last_name',
        'notes',
    )

    # Use raw ID widget for the account lookup (fast on large userbases)
    raw_id_fields = ('account',)

    # Reduce queries by fetching the related Account in one go
    list_select_related = ('account',)

    # Order newest additions first
    ordering = ('-added_on',)

    # Add a date drill-down by the added_on timestamp
    date_hierarchy = 'added_on'

    # How many items per page
    list_per_page = 25

    # Make added_on read-only in the detail view
    readonly_fields = ('added_on',)

    # Group fields into logical “panels” in the edit form
    fieldsets = (
        ('Player Account', {
            'fields': ('account',),
        }),
        ('Verification & Availability', {
            'fields': (
                'is_verified',
                'is_available',
                'current_activity',
            ),
        }),
        ('Additional Details', {
            'fields': (
                'notes',
                'added_on',
            ),
        }),
    )




@admin.register(FootballJob)
class FootballJobAdmin(UnfoldModelAdmin):
    list_display  = ('position_title', 'country_name', 'salary_offer', 'age_range', 'created_at')
    search_fields = ('country_name', 'position_title')
    list_filter   = ('country_name', 'created_at')



@admin.register(PlayerJobApplication)
class PlayerJobApplicationAdmin(UnfoldModelAdmin):
    list_display = (
        'full_name',
        'email_address',
        'current_club',
        'position',
        'job_link',
        'resume_link',
        'highlight_link',
        'status',  # Added status to the list display
        'submitted_at',
    )

    list_filter = (
        'current_club',
        'position',
        'job__position_title',
        'preferred_foot',
        'nationality',
        'status',  # Added status filter
    )

    search_fields = (
        'first_name', 'last_name', 'email_address',
        'current_club', 'position',
        'job__position_title',
    )

    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at',)

    fieldsets = (
        ('Job Applied For', {
            'fields': ('job',),
        }),
        ('Personal Details', {
            'fields': (
                'first_name', 'last_name', 'date_of_birth', 'nationality',
                'email_address', 'phone_number', 'address',
                'profile_image',
            ),
        }),
        ('Club & Career Info', {
            'fields': (
                'current_club', 'previous_clubs', 'position',
                'preferred_foot', 'height', 'weight',
                'coach_name', 'coach_contact',
            ),
        }),
        ('Media & Documents', {
            'fields': ('resume', 'player_video_link'),
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'status'),
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    def job_link(self, obj):
        if obj.job:
            url = getattr(obj.job, 'get_absolute_url', None) or f"/admin/yourapp/footballjob/{obj.job.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.job)
        return "-"
    job_link.short_description = 'Job'

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">Download CV</a>', obj.resume.url)
        return "-"
    resume_link.short_description = 'Resume'

    def highlight_link(self, obj):
        if obj.player_video_link:
            return format_html('<a href="{}" target="_blank">Watch Reel</a>', obj.player_video_link)
        return "-"
    highlight_link.short_description = 'Highlight Video'

    # Adding custom actions for approval/rejection
    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected applications have been approved.")

    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected applications have been rejected.")

    approve_applications.short_description = "Approve selected applications"
    reject_applications.short_description = "Reject selected applications"


@admin.register(ResetCode)
class ResetCodeAdmin(UnfoldModelAdmin):
    list_display = ("user", "reset_code", "reset_code_status", "reset_code_created_at")
    list_filter = ("reset_code_status",)  # ← Add trailing comma
    search_fields = ("user__username", "reset_code")
    readonly_fields = ("reset_code_created_at",)  # ← Add trailing comma

    def has_add_permission(self, request):
        """Disable manual addition from admin (codes should be generated automatically)."""
        return False

from django import forms
from .models import PlayerJobApplication

class PlayerJobApplicationForm(forms.ModelForm):
    class Meta:
        model = PlayerJobApplication
        exclude = ['job', 'submitted_at', 'user', 'status']  # 'status' will default to 'Pending'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Set required fields
        required_fields = [
            'date_of_birth',
            'nationality',
            'phone_number',
            'email_address',
        ]
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        if user:
            readonly_fields = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'nationality': user.nationality,
                'phone_number': user.phone_number,
                'email_address': user.email,
                'height': user.height,
                'weight': user.weight,
                'position': user.position,
                'preferred_foot': user.preferred_foot,
            }

            for field_name, value in readonly_fields.items():
                if value not in [None, '', 0] and field_name in self.fields:
                    self.fields[field_name].initial = value
                    self.fields[field_name].widget.attrs.update({
                        'readonly': True,
                        'style': 'background-color: #f5f5f5; cursor: not-allowed;',
                    })

            if 'profile_image' in self.fields and user.profile_image:
                self.fields['profile_image'].initial = user.profile_image

            self.instance.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Ensure default status is 'Pending'
        if not instance.status:
            instance.status = 'Pending'

        if not instance.user:
            raise ValueError("User must be set for the application")

        if commit:
            instance.save()
        return instance

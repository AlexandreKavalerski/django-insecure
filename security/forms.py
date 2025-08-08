from django import forms
from django.core.validators import RegexValidator

class SecureForm(forms.Form):
    """Base form with security measures"""
    def clean(self):
        cleaned_data = super().clean()
        # Add any common security validation here
        return cleaned_data

class UserInputForm(SecureForm):
    """Example form with secure input validation"""
    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s]*$',
                message='Only alphanumeric characters and spaces are allowed',
                code='invalid_name'
            )
        ]
    )
    email = forms.EmailField()
    message = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\.,!?@-]*$',
                message='Only alphanumeric characters and basic punctuation are allowed',
                code='invalid_message'
            )
        ]
    )

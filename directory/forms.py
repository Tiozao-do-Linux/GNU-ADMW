from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class UserCreationForm(forms.Form):
    """Form for creating new AD users"""
    
    # Username validation - alphanumeric and specific special characters only
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._-]+$',
        message='Username may only contain letters, numbers, dots, underscores and hyphens'
    )

    # Password validation
    def validate_password_complexity(value):
        """Custom validator for password complexity"""
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if not any(char.isupper() for char in value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in value):
            raise ValidationError('Password must contain at least one number')
        if not any(char in '!@#$%^&*()' for char in value):
            raise ValidationError('Password must contain at least one special character (!@#$%^&*())')

    # Form fields
    username = forms.CharField(
        max_length=50,
        validators=[username_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        help_text='Username for AD login (e.g., john.doe)'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        validators=[validate_password_complexity],
        help_text='Password must be at least 8 characters long and contain uppercase, lowercase, numbers and special characters'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )

    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter department'
        })
    )

    title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter job title'
        })
    )

    def clean(self):
        """Custom validation for the entire form"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')

        # Generate email if not provided
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if not email and username:
            # You can customize the domain as needed
            cleaned_data['email'] = f"{username}@yourdomain.com"

        return cleaned_data

class UserModificationForm(forms.Form):
    """Form for modifying existing AD users"""
    
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )

    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter department'
        })
    )

    title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter job title'
        })
    )

    enabled = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

class PasswordResetForm(forms.Form):
    """Form for resetting user passwords"""
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        validators=[UserCreationForm.validate_password_complexity],
        help_text='Password must be at least 8 characters long and contain uppercase, lowercase, numbers and special characters'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        """Custom validation for the entire form"""
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError('Passwords do not match')

        return cleaned_data

class UserSearchForm(forms.Form):
    """Form for searching users"""
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by username, name, or email',
            'aria-label': 'Search users'
        })
    )

    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by department'
        })
    )

    status = forms.ChoiceField(
        choices=[
            ('', 'All Users'),
            ('enabled', 'Enabled'),
            ('disabled', 'Disabled')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
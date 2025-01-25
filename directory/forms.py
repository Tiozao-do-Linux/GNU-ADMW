from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)  # Only required for creation
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Only required for creation
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    enabled = forms.BooleanField(required=False)

class GroupForm(forms.Form):
    display_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match")
        return cleaned_data
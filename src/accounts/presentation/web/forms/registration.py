from django import forms

from accounts.presentation.common.validators import (
    ValidateMaxAge,
    ValidateMinAge,
    validate_username
)


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Email', max_length=254, widget=forms.EmailInput, required=True
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        validators=[validate_username]
    )
    date_of_birth = forms.DateField(
        label='Date of birth',
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[ValidateMinAge(min_age=18), ValidateMaxAge(max_age=140)],
        required=True
    )
    password = forms.CharField(
        label='Password',
        max_length=128,
        widget=forms.PasswordInput,
        min_length=8,
        required=True
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        max_length=128,
        min_length=8,
        widget=forms.PasswordInput,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

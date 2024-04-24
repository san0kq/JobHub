from accounts.presentation.common.validators import (
    ValidateFileExtension,
    ValidateFileSize,
)
from django import forms


class ProfileEditForm(forms.Form):
    """
    Form for users to fill in data when editing their profile information.

    """

    first_name = forms.CharField(
        label='First name', min_length=3, max_length=150, required=True, strip=True
    )
    last_name = forms.CharField(
        label='Last name', min_length=3, max_length=150, required=True, strip=True
    )
    email = forms.EmailField(
        label='Email', max_length=254, widget=forms.EmailInput
    )
    phone = forms.CharField(
        label='Phone',
        max_length=13
    )
    avatar = forms.ImageField(
        label='Avatar',
        allow_empty_file=False,
        validators=[
            ValidateFileExtension(['jpg', 'jpeg', 'png']),
            ValidateFileSize(5_000_000),
        ],
        required=False,
    )
    telegram = forms.URLField(label='Telegram URL', required=False)
    linkedin = forms.URLField(label='LinkedIn URL', required=False)

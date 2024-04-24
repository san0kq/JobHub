from django import forms


class LoginForm(forms.Form):
    email_or_username = forms.CharField(
        label='Email or Username', max_length=254
    )
    password = forms.CharField(
        label='Password', max_length=128, widget=forms.PasswordInput
    )

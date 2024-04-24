from .login import LoginView
from .registration import RegistrationView, ConfirmEmailView
from .profile import ProfileEditView, ProfileView, AvatarDeleteView

__all__ = [
    'LoginView',
    'RegistrationView',
    'ConfirmEmailView',
    'ProfileEditView',
    'ProfileView',
    'AvatarDeleteView'
]

from django.urls import path

from accounts.presentation.web.views import (
    LoginView,
    RegistrationView,
    ConfirmEmailView,
    ProfileEditView,
    ProfileView,
    AvatarDeleteView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('confirmation/', ConfirmEmailView.as_view(), name='register_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/delete_avatar/<str:profile_type>', AvatarDeleteView.as_view(), name='delete_avatar')
]

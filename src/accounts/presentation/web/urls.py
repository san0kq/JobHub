from django.urls import path

from accounts.presentation.web.views import (
    LoginView,
    RegistrationView,
    ConfirmEmailView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path("confirmation/", ConfirmEmailView.as_view(), name="register_confirm"),
]

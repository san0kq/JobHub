from django.urls import path

from accounts.presentation.api_v1.views import UpdateProfileTypeAPIView

app_name = 'accounts_api_v1'

urlpatterns = [
    path('update_profile_type/', UpdateProfileTypeAPIView.as_view(), name='update_profile_type')
]

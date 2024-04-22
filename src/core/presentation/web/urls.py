from django.urls import path

from core.presentation.web.views import IndexView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]

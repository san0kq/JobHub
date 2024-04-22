from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('core.presentation.web.urls', namespace='core')),
    # path('', include('accounts.presentation.web.urls', namespace='accounts')),
    # path('api/v1/', include('core.presentation.api_v1.urls')),
    # path('api/v1/', include('accounts.presentation.api_v1.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from accounts.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('images/', include('images.urls')),
    path('accounts/social/', include('social_django.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

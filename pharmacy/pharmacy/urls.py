from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from content.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/content/news/', permanent=True)),
    path('admin/', admin.site.urls),
    path('content/', include('content.urls')),
    path('catalog/', include('catalog.urls')),
    path('users/', include('users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
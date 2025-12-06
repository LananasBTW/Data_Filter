from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Interface d'administration par défaut de Django
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
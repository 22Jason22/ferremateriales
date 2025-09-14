"""
URL configuration for ferremateriales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.inventory.views import catalog # Import the catalog view

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    # La URL para smart_selects no debe colisionar con /admin/
    path('chaining/', include('smart_selects.urls')),
    # URLs de API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # URLs para las vistas web (plantillas de visualización)
    path('inventario/', include(('apps.inventory.urls', 'inventory'), namespace='inventory')),
    path('catalogo/', catalog, name='catalog'), # Add the catalog URL
    path('clientes/', include(('apps.crm.urls', 'crm'), namespace='crm')),
    path('ventas/', include(('apps.sales.urls', 'sales'), namespace='sales')),
    # El resto de las URLs de la API
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/crm/', include('apps.crm.urls')),
    path('api/users/', include('apps.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

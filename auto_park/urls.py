"""auto_park URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import ManagerListView, EnterpriseListView, VehicleListView, my_view
from rest_framework.authtoken.views import obtain_auth_token

#import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('managers/', ManagerListView.as_view(), name='manager-list'),
    path('enterprises/', EnterpriseListView.as_view(), name='enterprise-list'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('token/', obtain_auth_token),
    path('my-view/', my_view, name='my-view'),
]


static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





"""
URL configuration for le_vikings_cars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include

#MEDIA_URL et MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter 

from users.views import UserViewsets,RegisterView,ProfileView
from addresses.views import AddressViewsets
from cars.views import CarViewsets,CarImageViewsets
from core.views import OriginCountryViewsets,MalaisianCityViewsets
from imports.views import ImportInfoViewsets
from orders.views import OrderViewsets,OrderItemViewsets

router=DefaultRouter()

router.register(r'users',UserViewsets)
router.register(r'addresses', AddressViewsets, basename='addresses')
router.register(r'cars',CarViewsets)   
router.register(r'cars_images',CarImageViewsets)
router.register(r'core_origincountry',OriginCountryViewsets)
router.register(r'core_malaisian',MalaisianCityViewsets)
router.register(r'imports',ImportInfoViewsets)
router.register(r'orders_order',OrderViewsets, basename='order')
router.register(r'orders_orderitem',OrderItemViewsets,basename='orderitem')

#pour fournir les endpoints d'authentification JWT de Django REST Framework SimpleJWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/profile/', ProfileView.as_view()),
    
    path('api/',include(router.urls)),
    
    path('api/payments/', include("payments.urls")),
    
    path('api/dashboard/', include("dashboard.urls")),
    
    path('api/imports/', include("imports.urls")),
    
    path('api/ia/', include("ai_assistant.urls")),
]

#MEDIA_URL et MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

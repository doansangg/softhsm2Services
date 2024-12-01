from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
# from django.conf.urls import url


# Standard
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'SoftHsm', views.SoftHsmViewSet, basename="SoftHsm")
#router.register('', views.SoftHsmViewSet)
# Standard
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
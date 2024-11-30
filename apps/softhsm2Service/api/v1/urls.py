from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
    path('', include(router.urls)),
]
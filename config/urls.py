from django.urls import include,path,re_path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger docs", # Standard
        default_version='v1.0', # Standard
        description="Swagger docs for SoftHsm2 Services", 
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

prefix = 'atnv/softhsm2/v1.0/' # Standard

urlpatterns = [
    path(prefix + 'admin/', admin.site.urls),
    re_path(prefix + r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path(prefix + 'student/', include("apps.student_api.api.v1.urls")), # Standard
    path(prefix + 'softhsm2/', include("apps.softhsm2Service.api.v1.urls")), # Standard
    
]

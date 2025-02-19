from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
from rest_framework.routers import DefaultRouter

from mailing.views import ClientViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Messaging Service API",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="example@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

client_router = DefaultRouter()
client_router.register('', ClientViewSet)

urlpatterns = [
    # docs urls
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # project urls
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('users/', include('users.urls')),
        path('mailing/', include('mailing.urls')),
        path('clients/', include(client_router.urls)),
    ])),

    # jwt auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

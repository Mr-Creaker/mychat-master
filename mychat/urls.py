# mychat/urls.py
from django.contrib import admin
from django.urls import path, include
from chat import views as chat_views
from django.urls import path, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Опис вашого API",
    ),
    public=True,
    permission_classes=[AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', chat_views.register, name='register'),
    path('chat/', chat_views.chat, name='chat'),
    path('online-users/', chat_views.online_users_view, name='online_users'),
    path('accounts/', include('django.contrib.auth.urls')),  # Provides login/logout.
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

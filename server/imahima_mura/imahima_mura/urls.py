"""imahima_mura URL Configuration

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
from django.urls import include,path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView

from .settings import DEBUG
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
  openapi.Info(
     title="イマヒマ村API",
     default_version='v1.0',
     description="イマヒマ村APIDOC",
     terms_of_service="https://www.xxx.com/api/",
     contact=openapi.Contact(email="test"),
     license=openapi.License(name="BSD License"),
  ),
  public=True,
  permission_classes=(permissions.AllowAny,) if DEBUG else (permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token),# トークン発行用

    # # allauth用
    # path('accounts/', include('allauth.urls')),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # # メールアドレスの確認メールを送らないなら以下2ついらなくなる
    # path('account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
    #      name='account_confirm_email'),
    # path('account-confirm-email/', include('allauth.urls')),
    # # allauth用終わり


    path('api/', include('imahima.urls')),
    #drf -yasgルーター
    path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

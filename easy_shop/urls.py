# -*- coding: utf-8 -*-
"""easy_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

#'mozilla_django_oidc'
from mozilla_django_oidc import views as oidc_views
# from easy_shop.authentication import views as auth_views

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    #'mozilla_django_oidc'
    path(
        "authorization-code/authenticate/",
        oidc_views.OIDCAuthenticationRequestView.as_view(),
        name="oidc_authentication_init",
    ),
    path(
        "authorization-code/callback/",
        oidc_views.OIDCAuthenticationCallbackView.as_view(),
        name="oidc_authentication_callback",
    ),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('authcriipto/', include('authcriipto.urls', namespace='authcriipto')),

    path('', include('listings.urls', namespace='listings')),

    # OAuth2
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('api-auth/', include('rest_framework.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns


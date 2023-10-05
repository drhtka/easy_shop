# -*- coding: utf-8 -*-
from django.urls import path

from .views import index_view, index_view_two  # , home_view, ApiEndpoint

app_name = 'authcriipto'

urlpatterns = [
    path('', index_view, name='index'),
    path('index_view_two/', index_view_two, name='indexx'),
    # path('home/', home_view, name='home'),
    # path('api/', ApiEndpoint.as_view(), name='api-endpoint')
]
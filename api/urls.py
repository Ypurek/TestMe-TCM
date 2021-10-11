from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path('auth/token', get_csrf_token, name='api_token'),
    path('auth/login', api_login, name='api_login'),
    path('auth/logout', api_logout, name='api_logout'),

    path('tests', api_tests, name='api_tests'),
    path('tests/<id>', api_test, name='api_test'),
    path('tests/<id>/status', update_test_status, name='api_set_test_status'),

    path('getstat/', api_stats, name='api_stats'),
]

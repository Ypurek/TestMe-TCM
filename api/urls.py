from django.urls import path
from api import views

urlpatterns = [
    path('auth/token', views.get_csrf_token, name='api_token'),
    path('auth/login', views.api_login, name='api_login'),
    path('auth/logout', views.api_logout, name='api_logout'),

    path('tests', views.api_test_cases, name='api_test_cases'),
    path('tests/<int:test_id>', views.api_test, name='api_test'),
    path('tests/<int:test_id>/status', views.update_test_status, name='api_set_test_status'),
    path('tests/new', views.api_new_test, name='api_new_test'),

    path('getstat', views.api_stats, name='api_stats'),

]

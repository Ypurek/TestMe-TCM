from django.contrib import admin
from django.urls import path
from tcm.views import testnrun, auth, demo

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', auth.register, name='register'),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),

    path('', testnrun.dashboard, name='home'),
    path('tests/', testnrun.test_cases, name='tests'),
    path('runs/', testnrun.test_runs, name='runs'),
    path('test/new', testnrun.new_test, name='new_test'),

    path('getstat/', testnrun.refresh_stats, name='refresh'),
    path('tests/<int:test_id>', testnrun.update_test, name='update'),
    path('tests/<int:test_id>/delete', testnrun.delete_test, name='delete'),
    path('tests/<int:test_id>/status', testnrun.update_test_status, name='set_status'),
    path('tests/upload', testnrun.upload_tests, name='upload'),
    path('tests/download', testnrun.download_tests, name='download'),

    path('lazytest/', testnrun.lazy_load_tests, name='lazy_test'),
    path('lazyrun/', testnrun.lazy_load_runs, name='lazy_run'),

    path('demo/', demo.dashboard, name='demo_pages'),
    path('demo/waitPage', demo.wait_page, name='wait_page'),
    path('demo/waitAjax', demo.wait_ajax, name='wait_ajax'),
    path('demo/crash', demo.crash, name='crash'),
]

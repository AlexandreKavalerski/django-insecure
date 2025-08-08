from django.urls import re_path

from . import views

urlpatterns = [
    # SQL injection (safe version)
    re_path('safe/users/(?P<user_id>.*)', views.safe_users, name='safe_users'),

    # Admin page (refactored for security)
    re_path('admin', views.admin_index, name='admin_index'),

    # Search (refactored for XSS protection)
    re_path('search', views.search, name='search'),
]
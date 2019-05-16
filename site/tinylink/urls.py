from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('login/?$', views.login_user, name='login'),
    path('logout', views.logout_view, name='logout'),
    re_path(r'^ajax/tinylink/?$', views.make_link, name='make_link'),
]
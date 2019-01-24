from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^login/?$', views.login_user, name='login'),
    url(r'^logout/?$', views.logout_user, name='logout'),
]

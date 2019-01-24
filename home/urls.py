from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index_home'),
    url(r'^inventory$', views.employee_inventory, name='employee_inventory'),
    url(r'^messages$', views.messages, name='messages'),



    
]

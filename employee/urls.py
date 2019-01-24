from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'employee'
urlpatterns = [
    path('employee/', views.index, name='index_employee'),
]

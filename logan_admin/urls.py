from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from home import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),

    url('^$', home_views.index, name="index"),
    url(r'^', include('home.urls'), name='home'), # /home + login/ urls
    url(r'^', include('employee.urls'), name='employee'),
    url(r'^accounts/', include('accounts.urls'), name='employee'),
]

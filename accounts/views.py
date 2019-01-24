from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User


def login_user(request, *args):
    logout(request)
    username = password = ''
    context = { 'title': "Login - Logan admin", 'login_faile': False }
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home:index_home'))
        else:
            context['login_failed'] = True
    return render(request, 'accounts/login.html', context)

def logout_user(request):
    return HttpResponseRedirect(reverse('accounts:login'))
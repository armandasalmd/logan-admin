from django.shortcuts import render
from django.http import Http404, HttpResponse


# Enployee index
def index(request):
    context = { 'title': 'Darbuotojo panelė - Logan' }
    return render(request, 'employee/index.html', context)

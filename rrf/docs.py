from django.shortcuts import render
from django.urls import path
from .models import DocModel

def documentation_view (request) :
    context = {'docs':DocModel.objects.all()}
    return render(request, 'documentation.html', context)


urlpatterns = [
    path('', documentation_view, name='docs')
]
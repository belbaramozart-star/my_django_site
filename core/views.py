from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    context = {'message': 'Hello world'}
    return render(request, "core/index.html", context)

def contact(request):
    context = {'message': 'Contact'}
    return render(request, "core/contact.html", context)


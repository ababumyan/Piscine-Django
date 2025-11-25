from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(request, 'base.html', {})

def display_view(request):
    return render(request, 'ex01_display.html', {})

def template_view(request):
    return render(request, 'ex01_template.html', {})

def django_view(request):
    return render(request, 'ex01_django.html', {})


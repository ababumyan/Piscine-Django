from django.urls import path , include
from .views import ex03_view

urlpatterns = [
    path('ex03/', ex03_view, name='ex03_view'),
]
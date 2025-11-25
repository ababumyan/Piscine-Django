from django.urls import path , include
from .views import ex00_view

urlpatterns = [
    path('ex00/', ex00_view, name='ex00_view'),
]
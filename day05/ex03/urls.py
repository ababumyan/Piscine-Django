from django.urls import path
from .views import populate,display

urlpatterns = [
    path('populate/', populate, name='populate'),
    path('display/', display, name='display'),
]
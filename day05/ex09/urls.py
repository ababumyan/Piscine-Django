from django.urls import path
from .views import display, insert_data

urlpatterns = [
    path('display/', display, name='display'),
    path('insert/', insert_data, name='insert_data'),
]
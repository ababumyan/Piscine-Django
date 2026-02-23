from django.urls import path

from .views import filter_movies,index,display,get_genders

urlpatterns = [
    path('', index, name='index'),
    path('filter_movies/', filter_movies, name='filter_movies'),
    path('get_genders/', get_genders, name='get_genders'),
    path('display/', display, name='display'),
]
from django.urls import path

from .views import filter_movies,index

urlpatterns = [
    path('', index, name='index'),
    path('filter_movies/', filter_movies, name='filter_movies'),
]
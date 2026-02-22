from django.urls import path
from .views import init, populate,display,remove_view,remove_by_title

urlpatterns = [
    path('init/', init, name='init'),
    path('populate/', populate, name='populate'),
    path('display/', display, name='display'),
    path('remove/', remove_view, name='remove'),
    path('remove/id/<str:title>/', remove_by_title, name='remove_episode'),
]
from django.urls import path
from .views import  populate ,remove_by_title,remove_view,display


urlpatterns = [
    path('populate/', populate, name='populate'),
    path('display/', display, name='display'),
    path('remove/', remove_view, name='remove'),
    path('remove/id/<str:title>/', remove_by_title, name='remove_episode'),
]
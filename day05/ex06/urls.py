from django.urls import path
from .views import init, populate, display,update_view,update_by_opening_crawl

urlpatterns = [
    path('init/', init, name='init'),
    path('populate/', populate, name='populate'),
    path('display/', display, name='display'),
    path('update/', update_view, name='update_view'),
    path('update/<str:title>/', update_by_opening_crawl, name='update_by_opening_crawl'),
]
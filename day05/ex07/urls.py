from django.urls import path
from .views import populate, display, update_view, update_by_title_opening_crawl

urlpatterns = [
    path('populate/', populate, name='populate'),
    path('display/', display, name='display'),
    path('update/', update_view, name='update_view'),
    path('update/<str:title>/', update_by_title_opening_crawl, name='update_by_title_opening_crawl'),
]
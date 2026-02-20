from .views  import index
from django.urls import path


urlpatterns = [
    path('init/', index, name='index'),
]
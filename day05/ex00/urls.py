from .views  import init
from django.urls import path


urlpatterns = [
    path('init/', init, name='init'),
]
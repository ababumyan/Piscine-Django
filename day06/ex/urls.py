from django.urls import path, include
from .views import index, get_random_user

urlpatterns = [
    path('', index, name='index'),
    path('get_random_user/', get_random_user, name='get_random_user'),
    path('auth/', include('ex.auth.urls')),
]
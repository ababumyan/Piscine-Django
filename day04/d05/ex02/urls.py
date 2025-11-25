from django.urls import path
from . import views

urlpatterns = [
    path('ex02/', views.ex02_view, name='ex02'),
]

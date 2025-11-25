from django.urls import path , include
from .views import index_view,django_view,template_view,display_view

urlpatterns = [
    path('ex01/', index_view, name='index_view'),
    path('ex01/django/', django_view, name='django_view'),
    path('ex01/templates/', template_view, name='template_view'),
    path('ex01/display/', display_view, name='display_view'),
]
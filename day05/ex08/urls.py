from django.urls import path
from .views import init ,update_table,populate,display

urlpatterns = [
    path('init/', init, name='init'),
    path('update/', update_table, name='update_table'),
    path('populate/', populate, name='populate'),
    path('display/', display, name='display'),

]
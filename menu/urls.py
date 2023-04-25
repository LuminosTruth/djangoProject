from django.urls import path
from menu.views import *

urlpatterns = [
    path('', home, name='home-page'),
    path('test/', home, name='test')
]

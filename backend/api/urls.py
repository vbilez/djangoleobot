from django.urls import path
from .views import *

urlpatterns =[
    path('dform', home),
    path('getnaspunkt.json',naspunkts),
    path('getrayonu.json',rayons),
    path('getvulyci.json',getvulyci)
]

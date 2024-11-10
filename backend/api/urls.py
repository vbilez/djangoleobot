from django.urls import path
from .views import *

urlpatterns =[
    path('dform', home),
    path('onform', onform),
    path('getnaspunkt.json',naspunkts),
    path('getrayonu.json',rayons),
    path('getvulyci.json',getvulyci),
    path('getnaspunktperedmistia.json',Naselenyipunktperedmistiaf),
    path('getvulyciperedmist.json',vulyciperedmist),
    path('getnevtags.json',nevtags),
    path('objectneruxomosti',neruxomobj),
    path('makeimage',makeimage),
    path('showobj/<int:id>/',showobj,name='showobj')
]

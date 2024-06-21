from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from api.models import Naspunkt,Rayon,Vulyci
from django.db.models import Q
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
# Create your views here.
def home(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def naspunkts(request):
    np = Naspunkt.objects.filter(Q(ID_type_nas_punkt= 1) | Q(ID_type_nas_punkt= 2) | Q(ID_type_nas_punkt= 3)).only('id', 'imja_nas_punkt')
    formatted_data = [
        {"label": item.imja_nas_punkt, "value": item.id}
        for item in np
    ]
        

    return JsonResponse(formatted_data, safe=False)

def rayons(request):
    qs = list(Rayon.objects.values('misto','id','Nazva_Rayona'))
    formatted_data = [
        {"misto": convertStrToInt(item['misto']),"label": item['Nazva_Rayona'], "value": item['id']}
        for item in qs
    ]
    #SomeModel_json = serializers.serialize("json", qs)
   
    return JsonResponse(formatted_data, safe=False)
def convertStrToInt(str):
    try:
        return int(str)
    except ValueError:
        return 0  # the default value
    
def getvulyci(request):
    qs =Vulyci.objects.values('IDrayons','id','Name_Vul')
    formatted_data = [
        {"label": item['Name_Vul'],  "value": item['id'],"link": convertStrToInt(item['IDrayons'])}
        for item in qs
    ]
    # SomeModel_json = serializers.serialize("json", qs)
   
    return JsonResponse(formatted_data, safe=False)



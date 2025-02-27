from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from api.models import Naspunkt,Rayon,Vulyci,Naselenyipunktperedmistia,Vulyciperedmist,Testobj,Objectneruxomosti,Images,Materialstin,Stan,Kstspalen,Budivlia,Nevtags,ObjectneruxomostiNevtag
from django.db.models import Q
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
import re
import base64
import uuid
# Create your views here.
def home(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def showobj(request,id):
  template1 = loader.get_template('object.html')
  obj = list(Objectneruxomosti.objects.filter(id=id).values())
  imgs = list(Images.objects.filter(idobject=id).values('name','dir'))
  matstin = list(Materialstin.objects.values('MaterialStin'))
  stanlist = list(Stan.objects.values('stan'))
  kstspalenlist = list(Kstspalen.objects.values('spalennazva'))
  budivlialist = list(Budivlia.objects.values('budivlia'))
  myobj = obj[0] if obj else None
  myt =myobj.get('materialstinid')
  matstinname = matstin[myt-1]
  stanid =myobj.get('stanid')
  stanname = stanlist[stanid-1]
  kstspalenid =myobj.get('kstspalenid')
  kstspalenname = kstspalenlist[kstspalenid-1]
  budivliaid  = myobj.get('typebydivliaid')
  budivlianame = budivlialist[budivliaid-1]
  nevtagsref = list(ObjectneruxomostiNevtag.objects.filter(objectneruxomosti_id =id).values('nevtag_id'))
  nevtagids=[]
  for ntag in nevtagsref:
      if isinstance(ntag,dict):
          nevtagids.append(ntag.get('nevtag_id'))
  tags=[]
  for tid in nevtagids:
     tt = list(Nevtags.objects.filter(id=tid).values('label'))
     tags.append( tt[0]['label'])
  context = {
        'id': id,  # You can pass your variable here
        'objectner': obj[0] if obj else None,
        'imgs':imgs,
        'matstin':matstin,
        'matstinname':matstinname,
        'myt':myt,
        'stanlist':stanlist,
        'stanname':stanname,
        'stanid':stanid,
        'kstspalenlist':kstspalenlist,
        'kstspalenid':kstspalenid,
        'kstspalenname':kstspalenname,
        'budivlialist':budivlialist,
        'budivliaid':budivliaid,
        'budivlianame':budivlianame,
        'tags':tags,

    }
  return HttpResponse(template1.render(context,request))


def onform(request):
  template = loader.get_template('onformmain.html')
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
    qs =Vulyci.objects.values('IDrayons','id','Name_Vul','misto')
    formatted_data = [
        {"label": item['Name_Vul'],  "value": item['id'],"link": convertStrToInt(item['IDrayons']),"misto":convertStrToInt(item['misto'])}
        for item in qs
    ]
    # SomeModel_json = serializers.serialize("json", qs)
   
    return JsonResponse(formatted_data, safe=False)

naspuntkperedmistialist = [

    'Винники',
    'Лисиничі',
    'Підбірці',
    'Волиця',
    'Бережани',
    'Давидів',
    'Пасіки Зубрецькі',
    'Зубра',
    'Мелечковичі',
    'Сокільники',
    'Солонка',
    'Нагоряни',
    'Наварія',
    'Скнилів',
    'Басівка',
    'Годовиця',
    'Лапаївка',
    'Зимна Вода',
    'Рудно',
    'Паланки',
    'Підрясне',
    'Кожичі',
    'Бірки',
    'Брюховичі',
    'Малехів',
    'Муроване',
    'Дубляни',
    'Гамаліівка',
    'Сороки Львівські',
    'інший населений пункт',


]
def Naselenyipunktperedmistiaf(request):
    qs =list(Naselenyipunktperedmistia.objects.filter().only('id','name'))

    formatted_data = [
        { "label": item.name,"value": convertStrToInt(item.id), }
        for item in qs
    ]

    return JsonResponse(formatted_data, safe=False)

def vulyciperedmist(request):
    qs =Vulyciperedmist.objects.values('id','name','idperedmistia')
    formatted_data = [
        {"label": item['name'],  "value": item['id'],"link": convertStrToInt(item['idperedmistia'])}
        for item in qs
    ]
    return JsonResponse(formatted_data, safe=False)

def nevtags(request):
    qs =list(Nevtags.objects.filter().only('label'))

    formatted_data = [
        { "label": item.label,"id":item.id }
        for item in qs
    ]

    return JsonResponse(formatted_data, safe=False)

@ensure_csrf_cookie
def neruxomobj(request):
    
    t = Testobj(jsonobj=request.body)
    t.save()
    prodazh11 = request.POST.get('prodazh', False)
    type_real_estate_post = request.POST.get('type_real_estate', '0')
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    value = body_data.get('prodazh', False)
    value2 = body_data.get('type_real_estate', 0)
    value3 = body_data.get('cina', 0)
    value4 = body_data.get('valuta', 1)
    value5 = body_data.get('kstspalen', 0)
    value6 = body_data.get('prysnachenniasemli', 0)
    value7 = body_data.get('ploshasagalnaa', 0)
    value8 = body_data.get('ploshakorysnaa', 0)
    value9 = body_data.get('ploshakuchniaa', 0)
    value10 = body_data.get('poverx', 0)
    value11 = body_data.get('poverxovist', 0)
    value12 = body_data.get('kstsanvusliv', 0)
    value13 = body_data.get('stan', 0)
    value14 = body_data.get('materialstin', 0)
    value15 = body_data.get('umebliovano', False)
    value16 = body_data.get('technika', False)
    value17 = body_data.get('umovuprodazhy', 0)
    value18 = body_data.get('dodatkovoproon', '0')
    value19 = int(body_data.get('budynoktype', 0) or 0)
    value20 = int(body_data.get('budivlia', 0) or 0)
    if body_data.get('naspunkt', 1)=='':
        npunkt =1
    else:
        npunkt =body_data.get('naspunkt', 1)["value"]
    value21 = npunkt
    value22 = body_data.get('rayon', 0)
    value23 = body_data.get('vulica', 0)
    value24 = body_data.get('budynok', 0)
    value25 = body_data.get('kvartyra', 0)
    value26 = body_data.get('korpus', '')
    value27 = body_data.get('opalenniaa','')
    value28 = body_data.get('doisd','')
    value29 = body_data.get('onimages',[])
    value30 = body_data.get('terminorendu',0)
    value31 = body_data.get('avtomiscetype',0)
    value32 = body_data.get('ploshadilianku', 0)
    value33 = body_data.get('komunikacii','')
    coordx = body_data.get('latstr', '')
    coordy = body_data.get('lngstr', '')
    linkedtagsids=[]
    if value2==1 and value==True:
        value7=0
        value8=0
        value9=0
        value10=0
        value11=0
        value12=0
        value13=0
        value14=0
        value27=0

    if value2==1 and value==False:
        value8=0
        value9=0
        value10=0
        value11=0
        value12=0
        value13=0
        value14=0
        value27=0
    if value2==4:
        value5=0
        value7=0
        value8=0
        value9=0
        value25=0
        value26=0
        nevtags=body_data.get('nev',[])



        for i in nevtags:
            print(type(i))
            if isinstance(i,dict):
                linkedtagsids.append(i.get("id"))
            if isinstance(i,str):
                nt = Nevtags(label=i)
                nt.save()
                linkedtagsids.append(nt.pk)

    if value2==5:
         value5=0
         value7=0
         value8=0
         value9=0
         value10=0
         value11=0
         value25=0
    if value2==6:
        value5=0
        value8=0
        value9=0
        value10=0
        value11=0
        value25=0
    if value==True:
        value30=0
    o = Objectneruxomosti(prodazh=value,
                          type_real_estate=value2,
                          cina=value3,
                          valuta=value4,
                          kstspalenid=value5,
                          prysnachenniasemliid=value6,
                          ploshasagalna=float(value7),
                          ploshakorysna=float(value8),
                          ploshakuchnia=float(value9),
                          poverx=value10,
                          poverxovist=value11,
                          kstsanvuslivid=value12,
                          stanid=value13,
                          materialstinid=value14,
                          umebliovano=value15,
                          technika=value16,
                          umovuprodashuid=value17,
                          dodatkovoproon=value18,
                          typebydunokid=value19,
                          typebydivliaid=value20,
                          mistoid=value21,
                          rayonid=value22,
                          vulicaid=value23,
                          bydunokaddr= value24,
                          kvartyraaddr=value25,
                          sectionaddr=value26,
                          opalennia=value27,
                          doisd = value28,
                          terminorendu=value30,
                          avtomiscetype=value31,
                          ploshadilianku=0.00 if value32 is None else float(value32),
                          komunikacii= value33,
                          coordx = coordx,
                          coordy = coordy,
                          )
    o.save()
    if value2==4:
        object_id= o.pk
        for item in linkedtagsids:
            oni =ObjectneruxomostiNevtag(objectneruxomosti_id =object_id,nevtag_id = item)
            oni.save()
    
    #if not value29:
    for item in value29:
            i = Images(name=item[1],dir=item[2],idobject=o.pk)
            i.save()

    
    return JsonResponse({"ok":json.loads(request.body)})

@ensure_csrf_cookie
def makeimage(request):

    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    imagedata = body_data.get('data')
    dir = body_data.get('dir')
    match = re.search(r"data:image/(.*?);", imagedata)
    if match:
        imgext = match.group(1)
    else:
        imgext = ''
    image = re.sub(r'data:image\/(.*?);base64,','',imagedata)
    imgdatadecoded = base64.b64decode(image)
    imgname = str(uuid.uuid4())+'.'+imgext
    filename = '../frontend/public/images/'+dir+'/'+ imgname # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdatadecoded)
    return JsonResponse({'id':imgext,'dir':dir,'imgfilename':filename,'imgname':imgname})

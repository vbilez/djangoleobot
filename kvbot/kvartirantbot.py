import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, callback_query,InputMediaPhoto, InputMediaVideo,InputFile,URLInputFile
import logging

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums import ParseMode

from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
import MySQLdb
import random
import tempfile
import copy

from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
import cyrtranslit

#database
hostname= 'localhost'
username = 'root'
passwordname = ''
dbname= 'reactdb'


inshyi = False

# північна частина передмістя 1
# південна частина передмістя 2
# західна частина передмістя 3
# східна частина пердемістя 4
mcon = MySQLdb.connect(host= hostname,user=username,passwd=passwordname,db=dbname)
cur = mcon.cursor()
cur.execute("SELECT * FROM naselenyipunktperedmistia LIMIT 29;")
res = cur.fetchall()
mcon.close()
# a = res.fetchall()
peredmistia_list = list(res)
peredmistia_listing =[]
for i in peredmistia_list:
    a=list(i)
    a.append(False)
    
    peredmistia_listing.append(a)

for item in peredmistia_listing:
    #print(cyrtranslit.to_latin(item[1], "ua") )
    peredmistia_listing_start=copy.deepcopy( peredmistia_listing)




async def showObjectsByFilter(data,callback):
    mcon = MySQLdb.connect(host= hostname,user=username,passwd=passwordname,db=dbname)
    cur = mcon.cursor()
    sql = "SELECT * FROM objectneruxomostis WHERE prodazh=1 AND type_real_estate=2 LIMIT 3;"
    try:
        cur.execute(sql )
        results = cur.fetchall()
        for row in results:
            print(row)
            #chat_id = callback.message.chat.id
            image = URLInputFile(
                "https://fastly.picsum.photos/id/19/2500/1667.jpg?hmac=7epGozH4QjToGaBf_xb2HbFTXoV5o8n_cYzB7I4lt6g",
                filename="python-logo.jpg"
            )
            image2 = URLInputFile(
                "https://fastly.picsum.photos/id/20/3670/2462.jpg?hmac=CmQ0ln-k5ZqkdtLvVO23LjVAEabZQx2wOaT4pyeG10I",
                filename="python-logo2.jpg"
            )
            media = [
                InputMediaPhoto(media=image, caption="Перше фото"),
                InputMediaPhoto(media=image2, caption="Друге фото"),
 
            ]
            await callback.bot.send_media_group(chat_id=callback.message.chat.id,media=media)

            await callback.message.answer(f"id:%s"%(row[0])+ "\n"+ f"продаж:%s"%(row[1])+ "\n"+ f"тип нерухомості:%s"%(row[2]))
        print("Data selected successfully.")
    except MySQLdb.Error as e:
        mcon.rollback()
    finally:
        cur.close()
        mcon.close()
def savefilter(kupivlia,uid, text,data):
    autoid=''
    mcon = MySQLdb.connect(host= hostname,user=username,passwd=passwordname,db=dbname)
    cur = mcon.cursor()

    if data['typeneruxomist']== 'квартира' and kupivlia==True:
        sql = "INSERT INTO savedfilter (userid,full,kupivlia,typeneruxomist,location,kstkimnat,typebydynok,stan,ploshakvartyry,comment,cinakvartyrakupivlia) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    
    
        try:
            cur.execute(sql, (uid, text,kupivlia,
                            data['typeneruxomist'] or '',
                            data['location'] or '',
                            data['kstkimnat']or '',
                            data['typebydynok']or '',
                            data['stan'] or '',
                            data['ploshakvartyry'] or '',
                            data['comment'] or '',
                            data['cinakvartyrakupivlia'] or '',
                            ))
            mcon.commit()
            print("Data inserted successfully.")
        except MySQLdb.Error as e:
            mcon.rollback()
        finally:
            cur.close()
            mcon.close()

    if data['typeneruxomist']== 'квартира' and kupivlia==False:
            sql = "INSERT INTO savedfilter (userid,full,kupivlia,typeneruxomist,location,kstkimnat,terminorendu,tvaryny,cina) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        
            try:
                cur.execute(sql, (uid, text,kupivlia,
                                data['typeneruxomist'] or '',
                                data['location'] or '',
                                data['kstkimnat'] or '',
                                data['terminorendu']or '',
                                data['tvaryny'] or '',
                                data['cina'] or '',
                                ))
                mcon.commit()
                print("Data inserted successfully.")
            except MySQLdb.Error as e:
                mcon.rollback()
            finally:
                cur.close()
                mcon.close()

    
    return


def form_keyboard_rayon_peredmistia_kupivlia(r,p,insh = False):
    global inshyi
    if insh==True:
        inshyi = not inshyi
    keyboard = []
    for button in r:
        keyboard.append(map_rayon_peredmist_kupivlia(button))


    n = len(p)
    previ = 0
    for i,button in enumerate(p):
        if i <previ+3 and  i >previ:
            continue
        if n>=3:
            keyboard.append(map_rayon_peredmistia_kupivlia(p[i:i+3],3))
            n=n-3
            previ=i
        

        if n==2:
            i=i+3
            keyboard.append(map_rayon_peredmistia_kupivlia(p[i:i+2],2))
            n=n-3
            previ=i
          
        if n==1:
            i=i+3
            keyboard.append(map_rayon_peredmistia_kupivlia(p[i:i+1],1))
            n=n-3
            previ=i
        
        if n<=0:
            break
    
        
    keyboard.append([InlineKeyboardButton(text=f'{field_checked(inshyi)}інший населений пункт',callback_data='inshyinaselenyipunkt')])        
    keyboard.append([InlineKeyboardButton(text=strilkavlivoe+'Назад',callback_data='stepbackrayonperedmistia_kupivlia'),InlineKeyboardButton(text='Далі'+strilkavpravoe,callback_data='stepforwardrayonperedmistia_kupivlia')])

    return keyboard

def filter_peredmistia(ch,listing):
    retresult=[]
    for el in listing:
        print(el)
        r1,r2,r3,r4 = el
        if(r3 in ch):
            retresult.append(el)
    # if ch:
    #      retresult.append([30,'інший населений пункт',1,False])
    return retresult

def change_rayon_peredmistia_kupivlia(loc='',ch=[],r=False):
   
     global peredmistia_listing
     global peredmistia_listing_start
     global rayon_checked_peredmist_kupivlia
     global rayon_checked_start_peredmist_kupivlia

     if(r==True):
         rn = rayon_checked_peredmist_kupivlia
         rm = rayon_checked_start_peredmist_kupivlia
     else:
         rn=[]
         rm=[]
     if loc=='start': 
        return form_keyboard_rayon_peredmistia_kupivlia(rm,filter_peredmistia(ch,peredmistia_listing_start))
  
     if loc == "Галицький": 
        rayon_checked_peredmist_kupivlia[0][1] = not rayon_checked_peredmist_kupivlia[0][1] 

        return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     if loc == "Франківський": 
        rayon_checked_peredmist_kupivlia[0][4] = not rayon_checked_peredmist_kupivlia[0][4] 
        return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     if loc == "Шевченківський": 
        rayon_checked_peredmist_kupivlia[1][1] = not rayon_checked_peredmist_kupivlia[1][1] 
        return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     if loc == "Сихівський": 
        rayon_checked_peredmist_kupivlia[1][4] = not rayon_checked_peredmist_kupivlia[1][4] 
        return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     if loc == "Личаківський": 
        rayon_checked_peredmist_kupivlia[2][1] = not rayon_checked_peredmist_kupivlia[2][1] 
        return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     if loc == "Залізничний": 
        rayon_checked_peredmist_kupivlia[2][4] = not rayon_checked_peredmist_kupivlia[2][4] 
        return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     for i,item in enumerate(peredmistia_listing):
        if loc ==peredmistia_listing[i][1]: 
            peredmistia_listing[i][3] = not peredmistia_listing[i][3] 
            return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing))
     if loc=='інший населений пункт':
         return form_keyboard_rayon_peredmistia_kupivlia(rn,filter_peredmistia(ch,peredmistia_listing),True)
     
def map_rayon_peredmistia_kupivlia(s3,a):
     if a==3:
        b1,b2,b3 = s3
        r1,r2,r3,r4 = b1
        r5,r6,r7,r8 = b2
        r9,r10,r11,r12 = b3

        return  [InlineKeyboardButton(text=f'{field_checked(r4)}{r2}',callback_data=f'{cyrtranslit.to_latin(r2, "ua")}'),InlineKeyboardButton(text=f'{field_checked(r8)}{r6}',callback_data=f'{cyrtranslit.to_latin(r6, "ua")}') ,InlineKeyboardButton(text=f'{field_checked(r12)}{r10}',callback_data=f'{cyrtranslit.to_latin(r10, "ua")}')]  
     if a==2:
         b1,b2 = s3
         r1,r2,r3,r4 = b1
         r5,r6,r7,r8 = b2
         return  [InlineKeyboardButton(text=f'{field_checked(r4)}{r2}',callback_data=f'{cyrtranslit.to_latin(r2, "ua")}'),InlineKeyboardButton(text=f'{field_checked(r8)}{r6}',callback_data=f'{cyrtranslit.to_latin(r6, "ua")}') ]  
     if a==1:
 
        b1 = s3[0]
        r1,r2,r3,r4 = b1
        
        return  [InlineKeyboardButton(text=f'{field_checked(r4)}{r2}',callback_data=f'{cyrtranslit.to_latin(r2, "ua")}')]   

leo_pryvit = 'Хвилька, все буде!\nбудьте ласкаві оберіть\nкритерії для пошуку\nщоб я швидко все пошукав\n\n\n'
wesearch = 'Ми шукаємо: '
typener = 'Тип нерухомості: '
rayonik = 'Район: '
locationtext = 'Локація: '
termin = 'Термін оренди: '
tvaryny = 'Домашні улюбленці: '
cinatext = 'Ціна, грн: '
cinatextdollar = 'Ціна, $: '
cinatexttysdollar = 'Ціна, тис.$: '
kimnattext = 'К-сть кімнат: '
vyd_vykorystanniatext = 'Вид використання: '
vyd_parkomisce = 'Вид машиномісця: '
typebydynoktext = 'Тип будинку: '
stantext = 'Стан: '
plkvartyry = 'Площа квартири, м2: '
plbydynku = 'Площа будинку, м2: '
commenttext = 'Коментар: '
vydbydunkutext ='Вид будинку: '
vydvykorystanniaselmliatext = 'Вид використання: '
kstsottext = 'Кількість соток: '
kstgatext = 'Кількість, Га: '
commenttextadv = 'Будь ласка, вкажіть важливі для Вас критерії або розкажіть про свою ідеальну квартиру: '
peredmistiatext ='Оберіть де бажаєте будинок: '
bydunokcomment = 'Розкажіть, будь ласка, про \nа також чого не повинно бути (наявність ділянки, ЖК, Вулиць тощо):  '
semliacomment = 'Будь ласка в довільній формі викладіть\n інформацію та критерії пошуку земельної ділянки: '
event1 = asyncio.Event()
saved_data = {}

strilkavlivo = '👈 '
strilkavpravo = ' 👉'
strilkavlivoe = '⬅ '
strilkavpravoe = ' ➡'

def field_checked(chk):
    if(chk==True): return '✅ '
    else :    return ''

class User(StatesGroup):
    user = State()

class Orenda(StatesGroup):
    orenda = State()
    typeneruxomist = State()
    location = State()
    kstkimnat = State()
    terminorendu = State()
    tvaryny = State()
    cina = State()
    vydvykorystannia = State()
    mashynomisce = State()
    cinamashynomisce = State()


class Kupivlia(StatesGroup):
    kupivlia=State()
    typeneruxomist = State()
    lvivandperedmistia = State()
    location = State()
    kstkimnat = State()
    typebydynok = State()
    vydbydynok = State()
    vydvykorystanniasemlia = State()
    stan = State()
    ploshakvartyry = State()
    ploshabydynky = State()
    ploshasemliasot = State()
    ploshasemliaga = State()
    cinakupivlia = State()
    vydvykorystannia = State()
    mashynomisce = State()
    cinamashynomisce = State()
    comment = State()
    cinakvartyrakupivlia = State()
    cinabydunokkupivlia = State()
    cinasemliakupivlia = State()
    kstsot= State()
    kstgaosg = State()
    kstgatorgivlia = State()




galic = False

kst_checked =[
    ["1k",False, "2k",False,],
    ["3k",False,"4k",False,]
]   

kst_checked_start =[
    ["1k",False, "2k",False,],
    ["3k",False,"4k",False,]
]  

kst_checked_kupivlia =[
    ["1k",False, "2k",False,],
    ["3k",False,"4k",False,]
]   

kst_checked_start_kupivlia =[
    ["1k",False, "2k",False,],
    ["3k",False,"4k",False,]
]  
    

kst_checked_bydunok_kupivlia =[
    ["1k",False, "2k",False,],
    ["3k",False,"4k",False,]
]   

kst_checked_bydunok_start_kupivlia =[
    ["1k",False, "2k",False,],
    ["3k",False,"4k",False,]
]  
   
    

rayon_checked_start = [["Галицький",False,"galickiy","Франківський",False,"frankivskij"],
                     ["Шевченківський",False,"shevchenkivskij","Сихівський",False,"syxivskij"],
                     ["Личаківський",False,"lychakivskij","Залізничний",False,"salisnichnij"],
    ]
rayon_checked = [["Галицький",False,"galickiy","Франківський",False,"frankivskij"],
                     ["Шевченківський",False,"shevchenkivskij","Сихівський",False,"syxivskij"],
                     ["Личаківський",False,"lychakivskij","Залізничний",False,"salisnichnij"],                    
    ]

lvivandperedmistia = [
                        ['Львів',True,"lvivandprlviv"],
                        ['Північна частина передмістя',False,"lvivandprpivnich"],
                        ['Південна частина передмістя',False,"lvivandprpivden"],
                        ['Західна частина передмістя',False,"lvivandprsaxid"],
                        ['Східна частина передмістя',False,"lvivandprsxid"],
                    ]

lvivandperedmistiastart = [
                        ['Львів',True,"lvivandprlviv"],
                        ['Північна частина передмістя',False,"lvivandprpivnich"],
                        ['Південна частина передмістя',False,"lvivandprpivden"],
                        ['Західна частина передмістя',False,"lvivandprsaxid"],
                        ['Східна частина передмістя',False,"lvivandprsxid"],
                    ]
rayon_checked_start_kupivlia = [["Галицький",False,"galickiykupivlia","Франківський",False,"frankivskijkupivlia"],
                     ["Шевченківський",False,"shevchenkivskijkupivlia","Сихівський",False,"syxivskijkupivlia"],
                     ["Личаківський",False,"lychakivskijkupivlia","Залізничний",False,"salisnichnijkupivlia"],
    ]
rayon_checked_kupivlia = [["Галицький",False,"galickiykupivlia","Франківський",False,"frankivskijkupivlia"],
                     ["Шевченківський",False,"shevchenkivskijkupivlia","Сихівський",False,"syxivskijkupivlia"],
                     ["Личаківський",False,"lychakivskijkupivlia","Залізничний",False,"salisnichnijkupivlia"],                    
    ]


rayon_checked_start_peredmist_kupivlia = [["Галицький",False,"galickiy_peredmist_kupivlia","Франківський",False,"frankivskij_peredmist_kupivlia"],
                     ["Шевченківський",False,"shevchenkivskij_peredmist_kupivlia","Сихівський",False,"syxivskij_peredmist_kupivlia"],
                     ["Личаківський",False,"lychakivskij_peredmist_kupivlia","Залізничний",False,"salisnichnij_peredmist_kupivlia"],
    ]
rayon_checked_peredmist_kupivlia = [["Галицький",False,"galickiy_peredmist_kupivlia","Франківський",False,"frankivskij_peredmist_kupivlia"],
                     ["Шевченківський",False,"shevchenkivskij_peredmist_kupivlia","Сихівський",False,"syxivskij_peredmist_kupivlia"],
                     ["Личаківський",False,"lychakivskij_peredmist_kupivlia","Залізничний",False,"salisnichnij_peredmist_kupivlia"],                    
    ]

def map_rayon(button):
     r1,r2,r3,r4,r5,r6 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r3}'),InlineKeyboardButton(text=f'{field_checked(r5)}{r4}',callback_data=f'{r6}')]

def map_rayon_kupivlia(button):
     r1,r2,r3,r4,r5,r6 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r3}'),InlineKeyboardButton(text=f'{field_checked(r5)}{r4}',callback_data=f'{r6}')]

def map_rayon_peredmist_kupivlia(button):

     r1,r2,r3,r4,r5,r6 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r3}'),InlineKeyboardButton(text=f'{field_checked(r5)}{r4}',callback_data=f'{r6}')]

def map_lviandperedmistia_kupivlia(button):
     r1,r2,r3 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r3}')]


def form_keyboard(rc):
    keyboard = []
    for button in rc:
        r1,r2,r3,r4,r5,r6 = button
        keyboard.append(map_rayon(button))

    keyboard.append([InlineKeyboardButton(text='Вибрати всі',callback_data='selectallrayons')],)
    keyboard.append([InlineKeyboardButton(text='Назад',callback_data='stepbackrayons'),InlineKeyboardButton(text='Далі',callback_data='stepforwardrayons')],)
    return keyboard

def form_keyboard_kupivlia(rc):
    keyboard = []
    for button in rc:
        r1,r2,r3,r4,r5,r6 = button
        keyboard.append(map_rayon_kupivlia(button))

    keyboard.append([InlineKeyboardButton(text='Вибрати всі',callback_data='selectallrayonskupivlia')],)
    keyboard.append([InlineKeyboardButton(text=strilkavlivo+'Назад',callback_data='stepbackrayonskupivlia'),InlineKeyboardButton(text='Далі'+strilkavpravo,callback_data='stepforwardrayonskupivlia')],)
    return keyboard


def form_keyboard_lvivandperedmistia_kupivlia(lc):
    keyboard = []
    for button in lc:
       # r1,r2,r3 = button
        keyboard.append(map_lviandperedmistia_kupivlia(button))

   
    keyboard.append([InlineKeyboardButton(text='Назад',callback_data='stepbacklvivandperedmistia_kupivlia'),InlineKeyboardButton(text='Далі',callback_data='stepforwardlvivandperedmistia_kupivlia')],)
    return keyboard

def change_rayon(rayon=''):
    global rayon_checked
    global rayon_checked_start
    if rayon=='start': 
        return form_keyboard(rayon_checked_start)
    if rayon == "Галицький": 
        rayon_checked[0][1] = not rayon_checked[0][1] 
        return form_keyboard(rayon_checked)
    if rayon == "Франківський": 
        rayon_checked[0][4] = not rayon_checked[0][4] 
        return form_keyboard(rayon_checked)
    if rayon == "Шевченківський": 
        rayon_checked[1][1] = not rayon_checked[1][1] 
        return form_keyboard(rayon_checked)
    if rayon == "Сихівський": 
        rayon_checked[1][4] = not rayon_checked[1][4] 
        return form_keyboard(rayon_checked)
    if rayon == "Личаківський": 
        rayon_checked[2][1] = not rayon_checked[2][1] 
        return form_keyboard(rayon_checked)
    if rayon == "Залізничний": 
        rayon_checked[2][4] = not rayon_checked[2][4] 
        return form_keyboard(rayon_checked)
    if rayon == 'all':
        rayon_checked[0][1]=True
        rayon_checked[0][4]=True
        rayon_checked[1][1]=True
        rayon_checked[1][4]=True
        rayon_checked[2][1]=True
        rayon_checked[2][4]=True
        return form_keyboard(rayon_checked)
    

def change_rayon_kupivlia(rayon=''):
    global rayon_checked_kupivlia
    global rayon_checked_start_kupivlia
    if rayon=='start': 
        return form_keyboard_kupivlia(rayon_checked_start_kupivlia)
    if rayon == "Галицький": 
        rayon_checked_kupivlia[0][1] = not rayon_checked_kupivlia[0][1] 
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    if rayon == "Франківський": 
        rayon_checked_kupivlia[0][4] = not rayon_checked_kupivlia[0][4] 
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    if rayon == "Шевченківський": 
        rayon_checked_kupivlia[1][1] = not rayon_checked_kupivlia[1][1] 
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    if rayon == "Сихівський": 
        rayon_checked_kupivlia[1][4] = not rayon_checked_kupivlia[1][4] 
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    if rayon == "Личаківський": 
        rayon_checked_kupivlia[2][1] = not rayon_checked_kupivlia[2][1] 
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    if rayon == "Залізничний": 
        rayon_checked_kupivlia[2][4] = not rayon_checked_kupivlia[2][4] 
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    if rayon == 'all':
        rayon_checked_kupivlia[0][1]=True
        rayon_checked_kupivlia[0][4]=True
        rayon_checked_kupivlia[1][1]=True
        rayon_checked_kupivlia[1][4]=True
        rayon_checked_kupivlia[2][1]=True
        rayon_checked_kupivlia[2][4]=True
        return form_keyboard_kupivlia(rayon_checked_kupivlia)
    





def change_lvivandperedmistia_kupivlia(locp=''):
    global lvivandperedmistia
    global lvivandperedmistiastart
    if locp=='start': 
        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistiastart)
    if locp == lvivandperedmistia[0][0]: 
        lvivandperedmistia[0][1] = not lvivandperedmistia[0][1] 
        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistia)
    
    if locp == lvivandperedmistia[1][0]: 
        lvivandperedmistia[1][1] = not lvivandperedmistia[1][1] 
        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistia)
    
    if locp == lvivandperedmistia[2][0]: 
        lvivandperedmistia[2][1] = not lvivandperedmistia[2][1] 
        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistia)
    
    if locp == lvivandperedmistia[3][0]: 
        lvivandperedmistia[3][1] = not lvivandperedmistia[3][1] 
        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistia)
    
    if locp == lvivandperedmistia[4][0]: 
        lvivandperedmistia[4][1] = not lvivandperedmistia[4][1] 
        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistia)

    if locp == 'all':
        lvivandperedmistia[0][1] = True
        lvivandperedmistia[1][1] = True
        lvivandperedmistia[2][1] = True
        lvivandperedmistia[3][1] = True
        lvivandperedmistia[4][1] = True

        return form_keyboard_lvivandperedmistia_kupivlia(lvivandperedmistia)

def form_rayonlist():
    global rayon_checked
    r=[]
    if rayon_checked[0][1]==True:
        r.append(rayon_checked[0][0])
    if rayon_checked[0][4]==True:
         r.append(rayon_checked[0][3])
    if rayon_checked[1][1]==True:
        r.append(rayon_checked[1][0])
    if rayon_checked[1][4]==True:
       r.append(rayon_checked[1][3])
    if rayon_checked[2][1]==True:
       r.append(rayon_checked[2][0])
    if rayon_checked[2][4]==True:
       r.append(rayon_checked[2][3])
    return ', '.join(r)


def form_rayonlist_kupivlia():
    global rayon_checked_kupivlia
    r=[]
    if rayon_checked_kupivlia[0][1]==True:
        r.append(rayon_checked_kupivlia[0][0])
    if rayon_checked_kupivlia[0][4]==True:
         r.append(rayon_checked_kupivlia[0][3])
    if rayon_checked_kupivlia[1][1]==True:
        r.append(rayon_checked_kupivlia[1][0])
    if rayon_checked_kupivlia[1][4]==True:
       r.append(rayon_checked_kupivlia[1][3])
    if rayon_checked_kupivlia[2][1]==True:
       r.append(rayon_checked_kupivlia[2][0])
    if rayon_checked_kupivlia[2][4]==True:
       r.append(rayon_checked_kupivlia[2][3])
    return ', '.join(r)


def form_lviandperedmistia_kupivlia():
    global lvivandperedmistia
    r=[]
    if lvivandperedmistia[0][1]==True:
        r.append(lvivandperedmistia[0][0])
    if lvivandperedmistia[1][1]==True:
         r.append(lvivandperedmistia[1][0])
    if lvivandperedmistia[2][1]==True:
        r.append(lvivandperedmistia[2][0])
    if lvivandperedmistia[3][1]==True:
       r.append(lvivandperedmistia[3][0])
    if lvivandperedmistia[4][1]==True:
       r.append(lvivandperedmistia[4][0])
   
    return ', '.join(r)


def form_rayon_peredmistia_kupivlia(insh=False):
    global peredmistia_listing
    global rayon_checked_peredmist_kupivlia
    r=[]
    if rayon_checked_peredmist_kupivlia[0][1]==True:
        r.append(rayon_checked_peredmist_kupivlia[0][0])
    if rayon_checked_peredmist_kupivlia[0][4]==True:
         r.append(rayon_checked_peredmist_kupivlia[0][3])
    if rayon_checked_peredmist_kupivlia[1][1]==True:
        r.append(rayon_checked_peredmist_kupivlia[1][0])
    if rayon_checked_peredmist_kupivlia[1][4]==True:
       r.append(rayon_checked_peredmist_kupivlia[1][3])
    if rayon_checked_peredmist_kupivlia[2][1]==True:
       r.append(rayon_checked_peredmist_kupivlia[2][0])
    if rayon_checked_peredmist_kupivlia[2][4]==True:
       r.append(rayon_checked_peredmist_kupivlia[2][3])
    for i,item in enumerate(peredmistia_listing):
        if peredmistia_listing[i][3]==True:
            r.append(peredmistia_listing[i][1])
    if inshyi==True:
        r.append('інший населений пункт')
   
    return ', '.join(r)



#  kst_checked[0][1]=True
#         kst_checked[0][3]=True
#         kst_checked[1][1]=True
#         kst_checked[1][3]=True
def form_kstlist():
    global kst_checked
    r=[]
    if kst_checked[0][1]==True:
        r.append('1к')
    if kst_checked[0][3]==True:
         r.append('2к')
    if kst_checked[1][1]==True:
        r.append('3к')
    if kst_checked[1][3]==True:
       r.append('4к +')
    return ', '.join(r)

def form_kstlist_kupivlia():
    global kst_checked_kupivlia
    r=[]
    if kst_checked_kupivlia[0][1]==True:
        r.append('1к')
    if kst_checked_kupivlia[0][3]==True:
         r.append('2к')
    if kst_checked_kupivlia[1][1]==True:
        r.append('3к')
    if kst_checked_kupivlia[1][3]==True:
       r.append('4к +')
    return ', '.join(r)

def form_kstlist_bydunok_kupivlia():
    global kst_checked_bydunok_kupivlia
    r=[]
    if kst_checked_bydunok_kupivlia[0][1]==True:
        r.append('1к')
    if kst_checked_bydunok_kupivlia[0][3]==True:
         r.append('2к')
    if kst_checked_bydunok_kupivlia[1][1]==True:
        r.append('3к')
    if kst_checked_bydunok_kupivlia[1][3]==True:
       r.append('4к +')
    return ', '.join(r)


def form_keyboard_kst(kst):
    keyboard = []
    for button in kst:

        keyboard.append(map_kst(button))

    keyboard.append([InlineKeyboardButton(text='Назад',callback_data='kststepback'),InlineKeyboardButton(text='Далі',callback_data='kstnext')],)

    return keyboard


def form_keyboard_kst_kupivlia(kst):
    keyboard = []
    for button in kst:

        keyboard.append(map_kst_kupivlia(button))

    keyboard.append([InlineKeyboardButton(text=strilkavlivoe+'Назад',callback_data='kststepback_kupivlia'),InlineKeyboardButton(text='Далі'+strilkavpravoe,callback_data='kstnext_kupivlia')],)

    return keyboard

def form_keyboard_kst_bydunok_kupivlia(kst):
    keyboard = []
    for button in kst:

        keyboard.append(map_kst_bydunok_kupivlia(button))

    keyboard.append([InlineKeyboardButton(text=strilkavlivoe+'Назад',callback_data='kststepback_bydunok_kupivlia'),InlineKeyboardButton(text='Далі'+strilkavpravoe,callback_data='kstnext_bydunok_kupivlia')],)

    return keyboard

def k4change (k4):
    if k4 == "4k":
        return "+"
    else:
        return ""
def map_kst(button):
     r1,r2,r3,r4 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r1[::-1]}'),InlineKeyboardButton(text=f'{field_checked(r4)}{r3}',callback_data=f'{r3[::-1]}')]


def map_kst_kupivlia(button):
     r1,r2,r3,r4 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r1[::-1]}kupivlia'),InlineKeyboardButton(text=f'{field_checked(r4)}{r3}{k4change(r3)}',callback_data=f'{r3[::-1]}kupivlia')]

def map_kst_bydunok_kupivlia(button):
     r1,r2,r3,r4 = button
     return  [InlineKeyboardButton(text=f'{field_checked(r2)}{r1}',callback_data=f'{r1[::-1]}bydunokkupivlia'),InlineKeyboardButton(text=f'{field_checked(r4)}{r3}{k4change(r3)}',callback_data=f'{r3[::-1]}bydunokkupivlia')]

def change_kst(kst=''):
    global kst_checked
    global kst_checked_start
    if kst=='start': 
        return form_keyboard_kst(kst_checked_start)
    if kst == "1k": 
        kst_checked[0][1] = not kst_checked[0][1] 
        return form_keyboard_kst(kst_checked)
    if kst == "2k": 
        kst_checked[0][3] = not kst_checked[0][3] 
        return form_keyboard_kst(kst_checked)
    if kst == "3k": 
        kst_checked[1][1] = not kst_checked[1][1] 
        return form_keyboard_kst(kst_checked)
    if kst == "4k": 
        kst_checked[1][3] = not kst_checked[1][3] 
        return form_keyboard_kst(kst_checked)

    if kst == 'all':
        kst_checked[0][1]=True
        kst_checked[0][3]=True
        kst_checked[1][1]=True
        kst_checked[1][3]=True

        return form_keyboard_kst(kst_checked)
    
def change_kst_kupivlia(kst=''):
    global kst_checked_kupivlia
    global kst_checked_start_kupivlia
    if kst=='start': 
        return form_keyboard_kst_kupivlia(kst_checked_start_kupivlia)
    if kst == "1k": 
        kst_checked_kupivlia[0][1] = not kst_checked_kupivlia[0][1] 
        return form_keyboard_kst_kupivlia(kst_checked_kupivlia)
    if kst == "2k": 
        kst_checked_kupivlia[0][3] = not kst_checked_kupivlia[0][3] 
        return form_keyboard_kst_kupivlia(kst_checked_kupivlia)
    if kst == "3k": 
        kst_checked_kupivlia[1][1] = not kst_checked_kupivlia[1][1] 
        return form_keyboard_kst_kupivlia(kst_checked_kupivlia)
    if kst == "4k": 
        kst_checked_kupivlia[1][3] = not kst_checked_kupivlia[1][3] 
        return form_keyboard_kst_kupivlia(kst_checked_kupivlia)

    if kst == 'all':
        kst_checked_kupivlia[0][1]=True
        kst_checked_kupivlia[0][3]=True
        kst_checked_kupivlia[1][1]=True
        kst_checked_kupivlia[1][3]=True

        return form_keyboard_kst_kupivlia(kst_checked_kupivlia)
    



def change_kst_bydunok_kupivlia(kst=''):
    global kst_checked_bydunok_kupivlia
    global kst_checked_bydunok_start_kupivlia
    if kst=='start': 
        
        return form_keyboard_kst_bydunok_kupivlia(kst_checked_bydunok_start_kupivlia)
    if kst == "1k": 
        kst_checked_bydunok_kupivlia[0][1] = not kst_checked_bydunok_kupivlia[0][1] 
        return form_keyboard_kst_bydunok_kupivlia(kst_checked_bydunok_kupivlia)
    if kst == "2k": 
        kst_checked_bydunok_kupivlia[0][3] = not kst_checked_bydunok_kupivlia[0][3] 
        return form_keyboard_kst_bydunok_kupivlia(kst_checked_bydunok_kupivlia)
    if kst == "3k": 
        kst_checked_bydunok_kupivlia[1][1] = not kst_checked_bydunok_kupivlia[1][1] 
        return form_keyboard_kst_bydunok_kupivlia(kst_checked_bydunok_kupivlia)
    if kst == "4k": 
        kst_checked_bydunok_kupivlia[1][3] = not kst_checked_bydunok_kupivlia[1][3] 
        return form_keyboard_kst_bydunok_kupivlia(kst_checked_bydunok_kupivlia)

    if kst == 'all':
        kst_checked_bydunok_kupivlia[0][1]=True
        kst_checked_bydunok_kupivlia[0][3]=True
        kst_checked_bydunok_kupivlia[1][1]=True
        kst_checked_bydunok_kupivlia[1][3]=True

        return form_keyboard_kst_bydunok_kupivlia(kst_checked_bydunok_kupivlia)




# type_bydynok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='будується',callback_data='bydyetsia')],
#     [InlineKeyboardButton(text='новобудова',callback_data='novobydova')],
#     [InlineKeyboardButton(text='українська забудова > 10 років',callback_data='ukrten')],
#     [InlineKeyboardButton(text='радянська забудова',callback_data='radianska')],
#     [InlineKeyboardButton(text='будинок старого Львова',callback_data='stariylviv')],
#     [InlineKeyboardButton(text='Назад',callback_data='typebydynokstepback'),InlineKeyboardButton(text='Далі',callback_data='typebydynokforward')],
    
#  ])

type_bydynok_kupivlia = [
    ['будується','bydyetsia',False],
    ['новобудова','novobydova',False],
    ['українська забудова > 10 років','ukrten',False],
    ['радянська забудова','radianska',False],
    ['будинок старого Львова','stariylviv',False],
]

def type_bydynok_keyboard():
    global type_bydynok_kupivlia
    keyboard = []
    for t,handl,v in type_bydynok_kupivlia:
        keyboard.append([InlineKeyboardButton(text=f'{field_checked(v)}{t}',callback_data=handl)])
    keyboard.append([InlineKeyboardButton(text='Назад',callback_data='typebydynokstepback'),InlineKeyboardButton(text='Далі',callback_data='typebydynokforward')],)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_type_bydynok_kupivlia():
    global type_bydynok_kupivlia
    r=[]
    for t,handl,v in type_bydynok_kupivlia:
        if v==True:
            r.append(t)
    return ', '.join(r)




vyd_vykorystannia_semlia_kupivlia_obj = [
    ['під забудову','vyd_vykorystannia_semlia_kupivlia_pidsabudovu',False],
    ['дачна','vyd_vykorystannia_semlia_kupivlia_dachna',False],
    ['ОСГ','vyd_vykorystannia_semlia_kupivlia_osg',False],
    ['промисловість','vyd_vykorystannia_semlia_kupivlia_promyslovist',False],
    ['торгівля','vyd_vykorystannia_semlia_kupivlia_torgivlia',False],
    ['інше','vyd_vykorystannia_semlia_kupivlia_inshe',False],
]

def calc_vyd_vykorystannia_semlia_kupivlia_choice():
    global vyd_vykorystannia_semlia_kupivlia_obj
    counter = 0
    for item in vyd_vykorystannia_semlia_kupivlia_obj:
        if item[2]==True:
            counter= counter +1 
    if counter==1:
        return True
    if vyd_vykorystannia_semlia_kupivlia_obj[0][2]==True and vyd_vykorystannia_semlia_kupivlia_obj[1][2]==True:
        return True
    return False

def vyd_vykorystannia_semlia_kupivlia_keyboard():
    global vyd_vykorystannia_semlia_kupivlia_obj
    keyboard = []
    for t,handl,v in vyd_vykorystannia_semlia_kupivlia_obj :
        keyboard.append([InlineKeyboardButton(text=f'{field_checked(v)}{t}',callback_data=handl)])
    c = calc_vyd_vykorystannia_semlia_kupivlia_choice()
    
    
    dali = InlineKeyboardButton(text='Далі',callback_data='vyd_vykorystannia_semlia_kupivlia_forward')
    prevnext = [InlineKeyboardButton(text='Назад',callback_data='vyd_vykorystannia_semlia_kupivlia_stepback')]
    if c:
        prevnext.append(dali)
    keyboard.append(prevnext)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def form_vyd_vykorystannia_semlia_kupivlia():
    global vyd_vykorystannia_semlia_kupivlia_obj 
    r=[]
    for t,handl,v in vyd_vykorystannia_semlia_kupivlia_obj:
        if v==True:
            r.append(t)
    return ', '.join(r)


def check_next_markup(vydvyk,step=1):
    if vydvyk=='':
        return None
    rosmitku=[]
    nexttext=[]
    vlst = vydvyk.split(',')
    if "під забудову" in vlst or "дачна" in vlst:
        rosmitku.append(kstsot_semlia_kupivlia_inline)
        nexttext.append(kstsottext)
    if "ОСГ" in vlst:
        rosmitku.append(kstga_osg_semlia_kupivlia_inline)
        if kstgatext not in nexttext:
            nexttext.append(kstgatext)
    if "промисловість" in vlst or "торгівля" in vlst:
        rosmitku.append(kstga_prom_semlia_kupivlia_inline)
        if kstgatext not in nexttext:
            nexttext.append(kstgatext)
    if "інше" in vlst:
        rosmitku.append(semlia_kupivlia_comment_inline)
        nexttext.append(semliacomment)
    return rosmitku[step-1],nexttext[step-1]    
        


loc_semlia_kupivlia = [
    ['Львів та до обʼїзної','lvivdoobj',False],
    ['до 10км від Львова','dotenvidlv',False],
    ['10-30 км від Львова','mishlviv',False],
    ['30 км і більше від Львова','thrirtypislialviv',False],
]


def loc_semlia_kupivlia_keyboard():
    global loc_semlia_kupivlia
    keyboard = []
    for t,handl,v in loc_semlia_kupivlia :
        keyboard.append([InlineKeyboardButton(text=f'{field_checked(v)}{t}',callback_data=handl)])
    keyboard.append([InlineKeyboardButton(text='Назад',callback_data='lvivlocselmlivakupivliastepback'),InlineKeyboardButton(text='Далі',callback_data='lvivlocselmlivakupivliaforward')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_loc_semlia_kupivlia():
    global loc_semlia_kupivlia 
    r=[]
    for t,handl,v in loc_semlia_kupivlia :
        if v==True:
            r.append(t)
    return ', '.join(r)




stan_kupivlia = [
    ['новий ремонт','novyiremont',False],
    ['хороший житловий','xoroshiyshitloviy',False],
    ['без ремонту','besremontu',False],
    ['від забудовника','vidsabudovnyka',False],

]





def stan_kupivlia_keyboard():
    global stan_kupivlia 
    keyboard = []
    for t,handl,v in stan_kupivlia :
        keyboard.append([InlineKeyboardButton(text=f'{field_checked(v)}{t}',callback_data=handl)])
    keyboard.append([InlineKeyboardButton(text=strilkavlivo+'Назад',callback_data='stanstepback'),InlineKeyboardButton(text='Далі'+strilkavpravo,callback_data='stanstepforward')],)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_stan_kupivlia():
    global stan_kupivlia 
    r=[]
    for t,handl,v in stan_kupivlia :
        if v==True:
            r.append(t)
    return ', '.join(r)



stan_bydunok_kupivlia = [
    ['новий ремонт','bydunoknovyiremont',False],
    ['хороший житловий','bydunokxoroshiyshitloviy',False],
    ['без ремонту','bydunokbesremontu',False],
    ['від забудовника','bydunokvidsabudovnyka',False],

]

def stan_bydunok_kupivlia_keyboard():
    global stan_bydunok_kupivlia 
    keyboard = []
    for t,handl,v in stan_bydunok_kupivlia:
        keyboard.append([InlineKeyboardButton(text=f'{field_checked(v)}{t}',callback_data=handl)])
    keyboard.append([InlineKeyboardButton(text=strilkavlivo+'Назад',callback_data='stanbydunokstepback'),InlineKeyboardButton(text='Далі'+strilkavpravo,callback_data='stanbydunokstepforward')],)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_stan_bydunok_kupivlia():
    global stan_bydunok_kupivlia 
    r=[]
    for t,handl,v in stan_bydunok_kupivlia :
        if v==True:
            r.append(t)
    return ', '.join(r)



bot =  Bot(token='mytoken')
dp = Dispatcher()


mmenu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Головне меню')],
    [KeyboardButton(text='Налаштувати бот')],
    [KeyboardButton(text='Збережені')],
    [KeyboardButton(text='Підтримка менеджера')],
]
,
resize_keyboard=True,
input_field_placeholder='Виберіть пункт меню'
)


# type_neruxomist_menu = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Кімната'), KeyboardButton(text='Квартира'),KeyboardButton(text='Будинок')],
#     [KeyboardButton(text='Комерція'),KeyboardButton(text='Машиномісце')],
# ]
# ,
# resize_keyboard=True,
# input_field_placeholder='Тип нерухомості:'
# )


#Main menu
mmenuinline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='орендувати',callback_data='orenduvatu')],
    [InlineKeyboardButton(text='купити',callback_data='kyputu')],
    [InlineKeyboardButton(text='здати',web_app=WebAppInfo(url='https://coins.42web.io/index.html'))],
    [InlineKeyboardButton(text='продати',callback_data='prodatu')],
    [InlineKeyboardButton(text='консультацію ⭐',callback_data='consultation')],
])
#callback_data='sdatu'

type_neruxomist_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кімната',callback_data='kimnata'),InlineKeyboardButton(text='Квартира',callback_data='kvartyra'),InlineKeyboardButton(text='Будинок',callback_data='bydunku')],
    [InlineKeyboardButton(text='Комерція',callback_data='komercia'),InlineKeyboardButton(text='Машиномісце',callback_data='carplace')],
    [InlineKeyboardButton(text='Назад',callback_data='stepback')]

])


type_neruxomist_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кімната',callback_data='kimnatakupivlia'),InlineKeyboardButton(text='Квартира',callback_data='kvartyrakupivlia')],
    [InlineKeyboardButton(text='Будинок',callback_data='bydunkukupivlia'),InlineKeyboardButton(text='Земля',callback_data='semliakupivlia')],
    [InlineKeyboardButton(text='Комерція',callback_data='komerciakupivlia'),InlineKeyboardButton(text='Машиномісце',callback_data='carplacekupivlia')],
    [InlineKeyboardButton(text='Назад',callback_data='stepbackkupivlia')]

])


terminorendu_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='До 3-х місяців',callback_data='dotermin')],
    [InlineKeyboardButton(text='3-6 місяців',callback_data='terminmish')],
    [InlineKeyboardButton(text='від 6 місяців',callback_data='terminpislia')],

    [InlineKeyboardButton(text='Назад',callback_data='kimnatastepback')],
    
 ])

#,InlineKeyboardButton(text='Далі',callback_data='termnext')


tvaryny_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Так',callback_data='tvarynytak'),InlineKeyboardButton(text='Ні',callback_data='tvarynyni')],
    [InlineKeyboardButton(text='Назад',callback_data='tvarynyprev')],
    
 ])


cina_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 3500',callback_data='cinado')],
    [InlineKeyboardButton(text='3500-5500',callback_data='cinamish')],
    [InlineKeyboardButton(text='від 5500',callback_data='cinapislia')],
     
    [InlineKeyboardButton(text='Назад',callback_data='cinaprev')],
 ])


cina_kimnata_kupivlia_inline  = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 12000',callback_data='cinadokimantakupivlia')],
    [InlineKeyboardButton(text='12000-18000',callback_data='cinamishkimantakupivlia')],
    [InlineKeyboardButton(text='18000',callback_data='cinapisliakimantakupivlia')],
     
    [InlineKeyboardButton(text='Назад',callback_data='cinaprevkimantakupivlia')],
 ])



cina_bydunok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 60',callback_data='cinadobydunokkupivlia'),InlineKeyboardButton(text='60 - 120',callback_data='cinamishbydunokkupivliafirst')],
    [InlineKeyboardButton(text='120-160',callback_data='cinamishbydunokkupivliasecond'),InlineKeyboardButton(text='160-240',callback_data='cinamishbydunokkupivliathird')],
    [InlineKeyboardButton(text='240-500',callback_data='cinapisliabydunokkupivliafour'),InlineKeyboardButton(text='500-900',callback_data='cinapisliabydunokkupivliafive')],
    [InlineKeyboardButton(text='900+',callback_data='cinapisliabydunokkupivlias')],
    [InlineKeyboardButton(text='Назад',callback_data='cinaprevbydunokkupivlia')],
 ])

# kskimnat_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text=f'{field_checked(kst_checked["1k"])}1к',callback_data='k1'),InlineKeyboardButton(text=f'{field_checked(kst_checked["2k"])}3к',callback_data='k2')],
#     [InlineKeyboardButton(text=f'{field_checked(kst_checked["3k"])}3к',callback_data='k3'),InlineKeyboardButton(text=f'{field_checked(kst_checked["4k"])}4к +',callback_data='k4')],

#     [InlineKeyboardButton(text='Назад',callback_data='kststepback'),InlineKeyboardButton(text='Далі',callback_data='kstnext')],
    
#  ])


cina_kvartyra_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 12000',callback_data='cinakvartyrado'),InlineKeyboardButton(text='12000 - 16000',callback_data='cinakvartyramishfirst')],
    [InlineKeyboardButton(text='16000 - 20000',callback_data='cinakvartyramishsecond'),InlineKeyboardButton(text='20000 - 25000',callback_data='cinakvartyramishthird')],
    [InlineKeyboardButton(text='25000 - 40000',callback_data='cinakvartyramishfour'),InlineKeyboardButton(text='від 40000',callback_data='cinakvartyramishpislia')],
    [InlineKeyboardButton(text='Назад',callback_data='cinakvartyrastepback')],
    
 ])

cina_bydunku_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 12000',callback_data='cinabydunkudo'),InlineKeyboardButton(text='12000 - 20000',callback_data='cinabydunkumishfirst')],
    [InlineKeyboardButton(text='20000 - 30000',callback_data='cinabydunkumishsecond'),InlineKeyboardButton(text='30000 - 50000',callback_data='cinabydunkumishthird')],
    [InlineKeyboardButton(text='від 50000',callback_data='cinabydunkumishpislia')],
    [InlineKeyboardButton(text='Назад',callback_data='cinabydunkustepback')],
    
 ])


cina_mashynomisce_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 3000',callback_data='cinamashynomiscedo')],
    [InlineKeyboardButton(text='3000 - 5000',callback_data='cinamashynomiscemish')],
    [InlineKeyboardButton(text='від 5000',callback_data='cinamashynomiscemishpislia')],
    [InlineKeyboardButton(text='Назад',callback_data='cinamashynomiscestepback')],
    
 ])


vyd_vykorystannia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Офіс',callback_data='ofis'),InlineKeyboardButton(text='Торгівля',callback_data='torgivlia')],
    [InlineKeyboardButton(text='HoReCa',callback_data='horeca'),InlineKeyboardButton(text='Склад',callback_data='sklad')],
    [InlineKeyboardButton(text='Виробництво',callback_data='vyrobnytstvo'),InlineKeyboardButton(text='Бізнес',callback_data='business')],
    [InlineKeyboardButton(text='Назад',callback_data='vydvykorystanniastepback')],
    
 ])

vyd_mashynomisce_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Гараж',callback_data='mashynomiscegarash'),InlineKeyboardButton(text='Паркомісце',callback_data='mashynomisceparkomisce')],

    [InlineKeyboardButton(text='Назад',callback_data='vydmashynomiscestepback')],
    
 ])


type_bydynok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='будується',callback_data='bydyetsia')],
    [InlineKeyboardButton(text='новобудова',callback_data='novobydova')],
    [InlineKeyboardButton(text='українська забудова > 10 років',callback_data='ukrten')],
    [InlineKeyboardButton(text='радянська забудова',callback_data='radianska')],
    [InlineKeyboardButton(text='будинок старого Львова',callback_data='stariylviv')],
    [InlineKeyboardButton(text='Назад',callback_data='typebydynokstepback'),InlineKeyboardButton(text='Далі',callback_data='typebydynokforward')],
    
 ])



stan_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='новий ремонт',callback_data='novyiremont')],
    [InlineKeyboardButton(text='хороший житловий',callback_data='xoroshiyshitloviy')],
    [InlineKeyboardButton(text='без ремонту',callback_data='besremontu')],
    [InlineKeyboardButton(text='від забудовника',callback_data='vidsabudovnyka')],

    [InlineKeyboardButton(text=strilkavlivo+'Назад',callback_data='stanstepback'),InlineKeyboardButton(text='Далі'+strilkavpravo,callback_data='stanstepforward')],
    
 ])

plosha_bydunok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 80',callback_data='ploshabydynokkupivliado'),InlineKeyboardButton(text='80-120',callback_data='ploshabydynokkupivliamishfirst')],
    [InlineKeyboardButton(text='120-180',callback_data='ploshabydynokkupivliamishsecond'),InlineKeyboardButton(text='180-250',callback_data='ploshabydynokkupivliamishthird')],
    [InlineKeyboardButton(text='250 і більше',callback_data='ploshabydynokkupivliapislia')],


    [InlineKeyboardButton(text='Назад',callback_data='ploshabydynokkupivliastepback')],
    
 ])


plosha_kvartyry_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 30',callback_data='ploshado'),InlineKeyboardButton(text='30-55',callback_data='ploshamishfirst')],
    [InlineKeyboardButton(text='55-75',callback_data='ploshamishsecond'),InlineKeyboardButton(text='75-100',callback_data='ploshamishthird')],
    [InlineKeyboardButton(text='100-150',callback_data='ploshamishfour'), InlineKeyboardButton(text='150 і більше',callback_data='ploshapislia')],


    [InlineKeyboardButton(text='Назад',callback_data='ploshastepback')],
    
 ])
# https://revenkroz.github.io/telegram-web-app-bot-example/index.html
comment_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='додати деталі' , web_app=WebAppInfo(url = 'https://vitalin.pythonanywhere.com/',))],
   
#    
    [InlineKeyboardButton(text='Назад',callback_data='commentstepback'),InlineKeyboardButton(text='Далі',callback_data='commentforward')],
    
 ])



bydunokcomment_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='додати деталі' , web_app=WebAppInfo(url = 'https://vitalin.pythonanywhere.com/',))],
    [InlineKeyboardButton(text=strilkavpravo+'Назад',callback_data='commentbydunokstepback'),InlineKeyboardButton(text='Далі'+strilkavlivo,callback_data='commentbydunokforward')],
    
 ])





cina_kvartyra_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 30',callback_data='cinakvartyrakupivliado'),InlineKeyboardButton(text='30-50',callback_data='cinakvartyrakupivliamishfirst')],
    [InlineKeyboardButton(text='50-70',callback_data='cinakvartyrakupivliamishsecond'),InlineKeyboardButton(text='70-100',callback_data='cinakvartyrakupivliamishthird')],
    [InlineKeyboardButton(text='100-140',callback_data='cinakvartyrakupivliamishfour'),InlineKeyboardButton(text='140-180',callback_data='cinakvartyrakupivliamishfifth')],
    [InlineKeyboardButton(text='180-250',callback_data='cinakvartyrakupivliamishsix'),InlineKeyboardButton(text='250+',callback_data='cinakvartyrakupivliapislia')],
    [InlineKeyboardButton(text='Назад',callback_data='cinakvartyrakupivliastepback')],
    
 ])


semlialocation_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='Львів та до обʼїзної',callback_data='lvivdoobj')],
 [InlineKeyboardButton(text='до 10км від Львова',callback_data='dotenvidlv')],
 [InlineKeyboardButton(text='10-30 км від Львова',callback_data='mishlviv')],
 [InlineKeyboardButton(text='30 км і більше від Львова',callback_data='thrirtypislialviv')],
 [InlineKeyboardButton(text='Назад',callback_data='lvivlocselmlivakupivliastepback'),InlineKeyboardButton(text='Далі',callback_data='lvivlocselmlivakupivliaforward'),]
])


vyd_vykorystannia_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='під забудову',callback_data='vyd_vykorystannia_semlia_kupivlia_pidsabudovu')],
 [InlineKeyboardButton(text='дачна',callback_data='vyd_vykorystannia_semlia_kupivlia_dachna')],
 [InlineKeyboardButton(text='ОСГ',callback_data='vyd_vykorystannia_semlia_kupivlia_osg')],
 [InlineKeyboardButton(text='промисловість',callback_data='vyd_vykorystannia_semlia_kupivlia_promyslovist')],
 [InlineKeyboardButton(text='торгівля',callback_data='vyd_vykorystannia_semlia_kupivlia_torgivlia')],
 [InlineKeyboardButton(text='інше',callback_data='vyd_vykorystannia_semlia_kupivlia_inshe')],
 [InlineKeyboardButton(text='Назад',callback_data='vyd_vykorystannia_semlia_kupivlia_stepback')],
])



kstsot_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='до 6',callback_data='kstsot_semlia_kupivlia_dosix')],
 [InlineKeyboardButton(text='6-10',callback_data='kstsot_semlia_kupivlia_sixten')],
 [InlineKeyboardButton(text='10-20',callback_data='kstsot_semlia_tentwenty')],
 [InlineKeyboardButton(text='від 20',callback_data='kstsot_semlia_kupivlia_fromtwenty')],
 [InlineKeyboardButton(text='Назад',callback_data='kstsot_semlia_kupivlia_stepback')],
])



cina_pidsabudovu_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='до 15',callback_data='cina_pidsabudovu_semlia_kupivlia_dofifteen')],
 [InlineKeyboardButton(text='15-30',callback_data='cina_pidsabudovu_semlia_kupivlia_fifteenthirty')],
 [InlineKeyboardButton(text='30-60',callback_data='cina_pidsabudovu_semlia_thirtysixty')],
 [InlineKeyboardButton(text='60-120',callback_data='cina_pidsabudovu_semlia_kupivlia_sixtyhundredtwenty')],
 [InlineKeyboardButton(text='120 і більше',callback_data='cina_pidsabudovu_semlia_kupivlia_fromhundredtwenty')],
 [InlineKeyboardButton(text='Назад',callback_data='cina_pidsabudovu_semlia_kupivlia_stepback'),InlineKeyboardButton(text='Далі',callback_data='cina_pidsabudovu_semlia_kupivlia_forward')],
])


kstga_osg_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='до 1',callback_data='kstga_osg_semlia_kupivlia_doone')],
 [InlineKeyboardButton(text='1-5',callback_data='kstga_osg_semlia_kupivlia_onefive')],
 [InlineKeyboardButton(text='5-20',callback_data='kstga_osg_semlia_fivetwenty')],
 [InlineKeyboardButton(text='20-50',callback_data='kstga_osg_semlia_kupivlia_twentyfifty')],
 [InlineKeyboardButton(text='50 і більше',callback_data='kstga_osg_semlia_kupivlia_fromfifty')],
 [InlineKeyboardButton(text='Назад',callback_data='kstga_osg_semlia_kupivlia_stepback')],
])



kstga_prom_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='до 0,5',callback_data='kstga_prom_semlia_kupivlia_dohalf')],
 [InlineKeyboardButton(text='0,5-1',callback_data='kstga_prom_semlia_kupivlia_halfone')],
 [InlineKeyboardButton(text='1-3',callback_data='kstga_prom_semlia_onetree')],
 [InlineKeyboardButton(text='3-10',callback_data='kstga_prom_semlia_kupivlia_treeten')],
 [InlineKeyboardButton(text='10 і більше',callback_data='kstga_prom_semlia_kupivlia_fromten')],
 [InlineKeyboardButton(text='Назад',callback_data='kstga_prom_semlia_kupivlia_stepback')],
])


semlia_kupivlia_comment_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='додати деталі' , web_app=WebAppInfo(url = 'https://vitalin.pythonanywhere.com/',))],
    [InlineKeyboardButton(text=strilkavlivo+'Назад',callback_data='comment_semlia_kupivliastepback'),InlineKeyboardButton(text='Далі'+strilkavpravo,callback_data='comment_semlia_kupivliaforward')],
 ])



test_contact_rpl = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='поділитись контактом' , request_contact=True)],
    
 ])

test_contact_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='поділитись контактом' , request_contact=True)],
    
 ])


filter_end = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фільтр збережено'+'✅',callback_data='filtercallback' )],
    
 ])

vydb =[
    ['особняк','osobniak_kupivlia',False],
    ['спарка','sparka_kupivlia',False],
    ['Таунхаус','taunxaus_kupivlia',False],
    ]


osobniak=False
taunxaus=False
sparka=False


def vydbkeyboard():
    keyboard = []
    for item in vydb:
       
        keyboard.append([InlineKeyboardButton(text=f'{field_checked(item[2])}{item[0]}',callback_data=f'{item[1]}')],)
    keyboard.append( [InlineKeyboardButton(text='Назад',callback_data='vydbydunkunkuprev'),InlineKeyboardButton(text='Далі',callback_data='vydbydunkunkunext'),],)
    return keyboard


vyd_bydunku_inline = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text=f'особняк',callback_data=f'osobniak_kupivlia')],
    [InlineKeyboardButton(text=f'спарка',callback_data=f'sparka_kupivlia')],
    [InlineKeyboardButton(text=f'Таунхаус',callback_data=f'taunxaus_kupivlia')],
    [InlineKeyboardButton(text='Назад',callback_data='vydbydunkunkuprev'),InlineKeyboardButton(text='Далі',callback_data='vydbydunkunkunext'),],
    
 ])

def form_vydbydunku_list():
    vb=[]
    if vydb[0][2]==True:
        vb.append(vydb[0][0])
    if vydb[1][2]==True:
        vb.append(vydb[1][0])
    if vydb[2][2]==True:
        vb.append(vydb[2][0])
    vbt = ', '.join(vb)
    return vbt





#location_inline = InlineKeyboardMarkup(inline_keyboard=change_rayon())
# @dp.chosen_inline_result(F.data=='webappcallback')

# async def check_data_handler(request: Request):
#     # bot: Bot = request.app["bot"]

#     data = await request.post()  # application/x-www-form-urlencoded
#     try:
#         data = safe_parse_webapp_init_data(token='7474259869:AAFPl-yO5Fx1JIt_DdL35dXZdq3JC56fzms', init_data=data["comment"])
#     except ValueError:
#         return json_response({"ok": False, "err": "Unauthorized"}, status=401)
#     return json_response({"ok": True, "data": data})


@dp.message(CommandStart())
async def cmd_start(message:Message, state:FSMContext):
    await state.clear()
    global rayon_checked 
    global rayon_checked_start
    global rayon_checked_kupivlia
    global rayon_checked_start_kupivlia
    rayon_checked = copy.deepcopy( rayon_checked_start)
    await state.set_state(User.user)
    await state.update_data(user=message)
    await message.answer_photo(photo='AgACAgIAAxkBAAMyZmA4k4XrW1ndOu09AfV8dzSg-4sAAu_bMRurSgFLzKEq3iEBwhEBAAMCAAN5AAM1BA',caption=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'+ ' ' + 'Ви хочете                                            .', reply_markup=mmenuinline,  parse_mode=ParseMode.HTML)


@dp.message(F.text == "/settings")
async def cmd_settings(message:Message):
    await message.answer('Налаштування ⚙')

@dp.message(F.text == "/saved")
async def cmd_settings(message:Message):
    await message.answer('Збережені 📝')

@dp.message(F.text == "/help")
async def cmd_settings(message:Message):
    await message.answer('Допомога менеджера ❔')





# async def webappcallback(callback:CallbackQuery, state:FSMContext,check_data_handler):
#     data = await state.get_data()
#     await callback.message.edit_caption( caption=leo_pryvit + wesearch + data["kupivlia"],parse_mode=ParseMode.HTML)


@dp.message(F.web_app_data)
async def webappdata( message:Message):

    await message.edit_caption(caption=str(message.web_app_data))
@dp.callback_query(F.data=='orenduvatu')
async def orenduvatu(callback:CallbackQuery, state:FSMContext):
    #await callback.answer('Ви вибрали орендувати')
    if (await state.get_state() == Orenda.orenda):
        data = await state.get_data()
        await callback.message.edit_caption( caption=leo_pryvit + wesearch + data["orenda"],reply_markup=type_neruxomist_inline)    
    else:
        await state.set_state(Orenda.orenda)
        await state.update_data(orenda = 'оренду')
        data = await state.get_data()
        await callback.message.edit_caption(photo='AgACAgIAAxkBAAMyZmA4k4XrW1ndOu09AfV8dzSg-4sAAu_bMRurSgFLzKEq3iEBwhEBAAMCAAN5AAM1BA' , caption=leo_pryvit + wesearch + data["orenda"],reply_markup=type_neruxomist_inline,parse_mode=ParseMode.HTML)
   # await callback.message.edit_text( leo_pryvit  + data["orenda"], )



@dp.callback_query(F.data=='kyputu')
async def kyputu(callback:CallbackQuery, state:FSMContext):
    #await callback.answer('Ви вибрали орендувати')
    if (await state.get_state() == Kupivlia.kupivlia):
        data = await state.get_data()
        await callback.message.edit_caption( caption=leo_pryvit + wesearch + data["kupivlia"],reply_markup=type_neruxomist_kupivlia_inline)    
    else:
        await state.set_state( Kupivlia.kupivlia)
        await state.update_data(kupivlia = 'купівля')
        data = await state.get_data()
        await callback.message.edit_caption(photo='AgACAgIAAxkBAAMyZmA4k4XrW1ndOu09AfV8dzSg-4sAAu_bMRurSgFLzKEq3iEBwhEBAAMCAAN5AAM1BA' , caption=leo_pryvit + wesearch + data["kupivlia"] + '\n' + typener,reply_markup=type_neruxomist_kupivlia_inline,parse_mode=ParseMode.HTML)

@dp.callback_query(F.data=='sdatu')
async def sdatu(callback:CallbackQuery):
    await callback.answer('Ви вибрали здати')
    await callback.message.answer('Здати ітд')

@dp.callback_query(F.data=='prodatu')
async def prodatu(callback:CallbackQuery):
    await callback.answer('Ви вибрали продати')
    await callback.message.answer('Продати ітд')

@dp.callback_query(F.data=='consultation')
async def consultation(callback:CallbackQuery):
    await callback.answer('Ви вибрали консультацію')
    await callback.message.answer('Консультацію ітд')

@dp.message(Orenda.orenda)
async def orenda(message:Message, state:FSMContext):
    pass

@dp.message(Orenda.typeneruxomist)
async def typeneruxomist(message:Message, state:FSMContext):
    pass

@dp.message(Orenda.location)
async def typeneruxomist(message:Message, state:FSMContext):
   #await state.update_data(location = form_rayonlist())
   #data = await state.get_data()
   pass

@dp.message(Orenda.terminorendu)
async def terminorendu(message:Message, state:FSMContext):
   #await state.update_data(location = form_rayonlist())
   
   #state.update_data(terminorendu='Не задано')
   #data = await state.get_data()
   #to = 'Не задано'
   #await message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + to, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
   pass

@dp.callback_query(F.data=='kimnata')
async def kimnata(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.typeneruxomist)
    await state.update_data(typeneruxomist = 'кімната')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kvartyra')
async def kvartyra(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.typeneruxomist)
    await state.update_data(typeneruxomist = 'квартира')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik  + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='bydunku')
async def bydunku(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.typeneruxomist)
    await state.update_data(typeneruxomist = 'будинок')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='komercia')
async def komercia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.typeneruxomist)
    await state.update_data(typeneruxomist = 'комерція')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='carplace')
async def carplace(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.typeneruxomist)
    await state.update_data(typeneruxomist = 'машиномісце')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='kimnatakupivlia')
async def kimnatakupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global rayon_checked_start_kupivlia
    rayon_checked_kupivlia = copy.deepcopy( rayon_checked_start_kupivlia)
    inmarkup = change_rayon_kupivlia('start')
    await state.set_state(Kupivlia.typeneruxomist)
    await state.update_data(typeneruxomist = 'кімната')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='kvartyrakupivlia')
async def kvartyrakupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global rayon_checked_start_kupivlia
    rayon_checked_kupivlia = copy.deepcopy( rayon_checked_start_kupivlia)
    inmarkup = change_rayon_kupivlia('start')
    await state.set_state(Kupivlia.typeneruxomist)
    await state.update_data(typeneruxomist = 'квартира')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='bydunkukupivlia')
async def bydunkukupivlia(callback:CallbackQuery, state:FSMContext):
    global lvivandperedmistia
    global lvivandperedmistiastart
    lvivandperedmistia = copy.deepcopy( lvivandperedmistiastart)
    inmarkup = change_lvivandperedmistia_kupivlia('start')
    await state.set_state(Kupivlia.typeneruxomist)
    await state.update_data(typeneruxomist = 'будинок')
    data = await state.get_data()
    loc = 'Львів'
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext + loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    pass

@dp.callback_query(F.data=='stepforwardlvivandperedmistia_kupivlia')
async def stepforwardlvivandperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    pm = form_lviandperedmistia_kupivlia()
    await state.update_data(lvivandperedmistia = pm)
    await state.set_state(Kupivlia.location)

    chpm = pm.split(',')

    ch =[]
    r=False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
     
        if el.strip() =='Південна частина передмістя':
            ch.append(2)
 
        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('start',ch,r)
    # inmarkup = change_rayon_peredmistia_kupivlia('start')
   
    
   

   
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ pm +'\n'+ locationtext, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)





@dp.callback_query(F.data=='galickiy_peredmist_kupivlia')
async def galickiy_peredmist_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    global rayon_checked_peredmist_kupivlia
   
    data = await state.get_data()
    #await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']

    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
  
        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Галицький',ch,r)

    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='frankivskij_peredmist_kupivlia')
async def frankivskij_peredmist_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    global rayon_checked_peredmist_kupivlia
   
    data = await state.get_data()
    #await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']

    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
  
        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Франківський',ch,r)

    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='shevchenkivskij_peredmist_kupivlia')
async def shevchenkivskij_peredmist_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    global rayon_checked_peredmist_kupivlia
   
    data = await state.get_data()
    #await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']

    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
  
        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Шевченківський',ch,r)

    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='syxivskij_peredmist_kupivlia')
async def syxivskij_peredmist_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    global rayon_checked_peredmist_kupivlia
   
    data = await state.get_data()
    #await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']

    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
  
        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Сихівський',ch,r)

    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='lychakivskij_peredmist_kupivlia')
async def lychakivskij_peredmist_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    global rayon_checked_peredmist_kupivlia
   
    data = await state.get_data()
    #await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']

    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
  
        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Личаківський',ch,r)

    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='salisnichnij_peredmist_kupivlia')
async def salisnichnij_peredmist_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    global rayon_checked_peredmist_kupivlia
   
    data = await state.get_data()
    #await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']

    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
  
        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Залізничний',ch,r)

    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='Vynnyky')
async def Vynnyky(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Винники',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Lysynyči")
async def Lysynyci(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Лисиничі',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='Pidbirci')
async def Pidbirci(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Підбірці',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='Volycja')
async def Volycja(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Волиця',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='Berežany')
async def Berežany(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Бережани',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='Davydiv')
async def Davydiv(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Давидів',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Pasiky Zubrec'ki")
async def PasikyZubrecki(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Пасіки Зубрецькі',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Zubra")
async def Zubra(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Зубра',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Melečkovyči")
async def Melečkovyči(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Мелечковичі',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Sokil'nyky")
async def Sokilnyky(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Сокільники',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Solonka")
async def Solonka(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Солонка',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Nahorjany")
async def Nahorjany(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Нагоряни',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Navarija")
async def Navarija(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Наварія',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Sknyliv")
async def Sknyliv(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Скнилів',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=="Basivka")
async def Basivka(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Басівка',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Hodovycja")
async def Hodovycja(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Годовиця',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=="Lapaïvka")
async def Lapaivka(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Лапаївка',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Zymna Voda")
async def ZymnaVoda(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Зимна Вода',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Rudne")
async def Rudne(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Рудне',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Palanky")
async def Palanky(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Паланки',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Pidrjasne")
async def Pidrjasne(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Підрясне',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Kožyči")
async def Kožyči(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Кожичі',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Birky")
async def Birky(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Бірки',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    

@dp.callback_query(F.data=="Brjuxovyči")
async def Brjuxovyči(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Брюховичі',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Malexiv")
async def Malexiv(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Малехів',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Murovane")
async def Murovane(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Муроване',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Dubljany")
async def Dubljany(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Дубляни',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="Hamaliivka")
async def Hamaliivka(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Гамаліівка',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="Soroky L'vivs'ki")
async def SorokyLvivski(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('Сороки Львівські',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="inshyinaselenyipunkt")
async def inshyinaselenyipunkt(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    global peredmistia_listing_start
    print('toogle')
    data = await state.get_data()
    await state.set_state(Kupivlia.location)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('інший населений пункт',ch,r)
    lc= form_rayon_peredmistia_kupivlia(True)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="stepforwardrayonperedmistia_kupivlia")
async def stepforwardrayonperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing

    data = await state.get_data()
    await state.set_state(Kupivlia.kstkimnat)
    pm = data['lvivandperedmistia']
    chpm = pm.split(',')
    ch =[]
    r= False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)

        if el.strip() =='Південна частина передмістя':
            ch.append(2)

        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_kst_bydunok_kupivlia('start')


    # change_rayon_peredmistia_kupivlia('Лисиничі',ch,r)
    lc= form_rayon_peredmistia_kupivlia()
    await state.update_data(location=lc)
    # if lc =='':
        #малтіпл для всіх передмість
        # selectallreq()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + lc + '\n'+ kimnattext, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="k1bydunokkupivlia")
async def stepforwardrayonperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    data = await state.get_data()
    inmarkup = change_kst_bydunok_kupivlia('1k')
    kt = form_kstlist_bydunok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + kt, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    

@dp.callback_query(F.data=="k2bydunokkupivlia")
async def stepforwardrayonperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    data = await state.get_data()
    inmarkup = change_kst_bydunok_kupivlia('2k')
    kt = form_kstlist_bydunok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + kt, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="k3bydunokkupivlia")
async def stepforwardrayonperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    data = await state.get_data()
    inmarkup = change_kst_bydunok_kupivlia('3k')
    kt = form_kstlist_bydunok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + kt, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="k4bydunokkupivlia")
async def stepforwardrayonperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    data = await state.get_data()
    inmarkup = change_kst_bydunok_kupivlia('4k')
    kt = form_kstlist_bydunok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + kt, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="kstnext_bydunok_kupivlia")
async def kstnext_bydunok_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global peredmistia_listing
    data = await state.get_data()

    kt = form_kstlist_bydunok_kupivlia()
    if kt=='':
        kt='1к,2к,3к,4к+'
    await state.update_data(kstkimnat=kt)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + kt + '\n' + vydbydunkutext, reply_markup=vyd_bydunku_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="kststepback_bydunok_kupivlia")
async def kststepback_bydunok_kupivlia(callback:CallbackQuery, state:FSMContext):

    global peredmistia_listing
    global peredmistia_listing_start
    data = await state.get_data()
    pm = form_lviandperedmistia_kupivlia()

   

    chpm = pm.split(',')

    ch =[]
    r=False
    for el in chpm:
        if el.strip() =='Львів':
            r=True
        if el.strip() =='Північна частина передмістя':
            ch.append(1)
     
        if el.strip() =='Південна частина передмістя':
            ch.append(2)
 
        if el.strip() =='Західна частина передмістя':
            ch.append(3)

        if el.strip() =='Східна частина передмістя':
            ch.append(4)

    inmarkup = change_rayon_peredmistia_kupivlia('start',ch,r)

    await state.update_data(location='')
    await state.set_state(Kupivlia.location)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext,  reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)




@dp.callback_query(F.data=="stepbackrayonperedmistia_kupivlia")
async def stepbackrayonperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    inmarkup = change_lvivandperedmistia_kupivlia('start')
    loc='Львів'
    await state.update_data(lvivandperedmistia=loc)
    await state.set_state(Kupivlia.lvivandperedmistia)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+loc,  reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

# osobniak=False
# taunxaus=False
# sparka=False
# vyd_bydunku_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='особняк',callback_data='osobniak_kupivlia')],
#     [InlineKeyboardButton(text='спарка',callback_data='sparka_kupivlia')],
#     [InlineKeyboardButton(text='Таунхаус',callback_data='taunxaus_kupivlia')],
# [InlineKeyboardButton(text='Назад',callback_data='vydbydunkunkuprev'),InlineKeyboardButton(text='Далі',callback_data='vydbydunkunkunext'),],
@dp.callback_query(F.data=="vydbydunkunkunext")
async def vydbydunkunkunext(callback:CallbackQuery, state:FSMContext):

    data = await state.get_data()

    vbt = form_vydbydunku_list()
    if vbt =='':
         vbt = 'особняк, спарка, Таунхаус'
    await state.update_data(vydbydynok=vbt)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + vbt + '\n' + stantext, reply_markup=stan_bydunok_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="vydbydunkunkuprev")
async def vydbydunkunkuprev(callback:CallbackQuery, state:FSMContext):

    data = await state.get_data()

    await state.update_data(kstkimnat='')

    inmarkup = change_kst_bydunok_kupivlia('start')

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="osobniak_kupivlia")
async def osobniak_kupivlia(callback:CallbackQuery, state:FSMContext):
 
    global vydb
    data = await state.get_data()
    vydb[0][2]= not vydb[0][2]
    vbt = form_vydbydunku_list()
    inmarkup = vydbkeyboard()
    await state.update_data(vydbydynok = vbt)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + vbt,  reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="sparka_kupivlia")
async def sparka_kupivlia(callback:CallbackQuery, state:FSMContext):
    global vydb
    data = await state.get_data()
    vydb[1][2]= not vydb[1][2]
    vbt = form_vydbydunku_list()
    inmarkup = vydbkeyboard()
    await state.update_data(vydbydynok = vbt)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + vbt,  reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="taunxaus_kupivlia")
async def taunxaus_kupivlia(callback:CallbackQuery, state:FSMContext):
    global vydb
    data = await state.get_data()
    vydb[2][2]= not vydb[2][2]
    vbt = form_vydbydunku_list()
    inmarkup = vydbkeyboard()
    await state.update_data(vydbydynok = vbt)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + vbt,  reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="bydunoknovyiremont")
async def bydunoknovyiremont(callback:CallbackQuery, state:FSMContext):
    global stan_bydunok_kupivlia
    data = await state.get_data()
    stan_bydunok_kupivlia[0][2]= not stan_bydunok_kupivlia[0][2]
    st = form_stan_bydunok_kupivlia()
    inmarkup = stan_bydunok_kupivlia_keyboard()
    await state.update_data(stan = st)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +st,  reply_markup=stan_bydunok_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="bydunokxoroshiyshitloviy")
async def bydunokxoroshiyshitloviy(callback:CallbackQuery, state:FSMContext):
    global stan_bydunok_kupivlia
    data = await state.get_data()
    stan_bydunok_kupivlia[1][2]= not stan_bydunok_kupivlia[1][2]
    st = form_stan_bydunok_kupivlia()
    inmarkup = stan_bydunok_kupivlia_keyboard()
    await state.update_data(stan = st)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +st,  reply_markup=stan_bydunok_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="bydunokbesremontu")
async def bydunokbesremontu(callback:CallbackQuery, state:FSMContext):
    global stan_bydunok_kupivlia
    data = await state.get_data()
    stan_bydunok_kupivlia[2][2]= not stan_bydunok_kupivlia[2][2]
    st = form_stan_bydunok_kupivlia()
    inmarkup = stan_bydunok_kupivlia_keyboard()
    await state.update_data(stan = st)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +st,  reply_markup=stan_bydunok_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="bydunokvidsabudovnyka")
async def bydunokvidsabudovnyka(callback:CallbackQuery, state:FSMContext):
    global stan_bydunok_kupivlia
    data = await state.get_data()
    stan_bydunok_kupivlia[3][2]= not stan_bydunok_kupivlia[3][2]
    st = form_stan_bydunok_kupivlia()
    inmarkup = stan_bydunok_kupivlia_keyboard()
    await state.update_data(stan = st)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +st,  reply_markup=stan_bydunok_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="stanbydunokstepforward")
async def stanbydunokstepforward(callback:CallbackQuery, state:FSMContext):
    global stan_bydunok_kupivlia
    data = await state.get_data()

    st = form_stan_bydunok_kupivlia()
    if st == '':
        st ='новий ремонт, хороший житловий, без ремонту, від забудовника'

    await state.update_data(stan = st)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext + st + '\n'+ plbydynku ,  reply_markup=plosha_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=="stanbydunokstepback")
async def stanbydunokstepforward(callback:CallbackQuery, state:FSMContext):
    global stan_bydunok_kupivlia
    data = await state.get_data()

    st = form_stan_bydunok_kupivlia()
    await state.update_data(vydbydynok ='')
    global vydb
    for i,item in enumerate(vydb):
        vydb[i][2]=False
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext,  reply_markup=vyd_bydunku_inline, parse_mode= ParseMode.HTML)

# plosha_bydunok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='до 80',callback_data='ploshabydynokkupivliado'),InlineKeyboardButton(text='80-120',callback_data='ploshabydynokkupivliamishfirst')],
#     [InlineKeyboardButton(text='120-180',callback_data='ploshabydynokkupivliamishsecond'),InlineKeyboardButton(text='180-250',callback_data='ploshabydynokkupivliamishthird')],
#     [InlineKeyboardButton(text='250 і більше',callback_data='ploshabydynokkupivliapislia')],


#     [InlineKeyboardButton(text='Назад',callback_data='ploshabydynokkupivliastepback')],
    
#  ])


@dp.callback_query(F.data=="ploshabydynokkupivliado")
async def ploshabydynokkupivliado(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    pl =  'до 80'
    await state.update_data(ploshabydynky = pl )
    
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku + pl + '\n' +bydunokcomment,  reply_markup=bydunokcomment_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="ploshabydynokkupivliamishfirst")
async def ploshabydynokkupivliamishfirst(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    pl =  '80-120'
    await state.update_data(ploshabydynky = pl )
    
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku + pl + '\n' +bydunokcomment,  reply_markup=bydunokcomment_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="ploshabydynokkupivliamishsecond")
async def ploshabydynokkupivliamishsecond(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    pl =  '120-180'
    await state.update_data(ploshabydynky = pl )
    
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku + pl + '\n' +bydunokcomment,  reply_markup=bydunokcomment_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="ploshabydynokkupivliamishthird")
async def ploshabydynokkupivliamishthird(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    pl =  '180-250'
    await state.update_data(ploshabydynky = pl )
    
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku + pl + '\n' +bydunokcomment,  reply_markup=bydunokcomment_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="ploshabydynokkupivliapislia")
async def ploshabydynokkupivliapislia(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    pl =  '250 і більше'
    await state.update_data(ploshabydynky = pl )
    
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku + pl + '\n' +bydunokcomment,  reply_markup=bydunokcomment_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="commentbydunokstepback")
async def commentbydunokstepback(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()

    await state.update_data(ploshabydynky =  '')
    
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku,  reply_markup=plosha_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=="commentbydunokforward")
async def commentbydunokforward(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()


    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=="ploshabydynokkupivliastepback")
async def ploshabydynokkupivliastepback(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    await state.update_data(stan = '')
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext ,  reply_markup=stan_bydunok_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="cinadobydunokkupivlia")
async def cinadobydunokkupivlia(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = 'до 60'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=="cinamishbydunokkupivliafirst")
async def cinamishbydunokkupivliafirst(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = '60 - 120'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=="cinamishbydunokkupivliasecond")
async def cinamishbydunokkupivliasecond(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = '120-160'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="cinamishbydunokkupivliathird")
async def cinamishbydunokkupivliathird(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = '160-240'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="cinapisliabydunokkupivliafour")
async def cinapisliabydunokkupivliafour(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = '240-500'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="cinapisliabydunokkupivliafive")
async def cinapisliabydunokkupivliafive(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = '500-900'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="cinapisliabydunokkupivlias")
async def cinapisliabydunokkupivlias(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    cinb = '900+'
    await state.update_data(cinabydunokkupivlia = cinb)

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  reply_markup=cina_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр===>'+'\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku  + data["ploshabydynky"] + '\n' + cinatexttysdollar + cinb,  parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=="cinaprevbydunokkupivlia")
async def cinaprevbydunokkupivlia(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    await state.update_data(ploshabydynky = '')

    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext+ data["lvivandperedmistia"] +'\n'+ locationtext + data["location"] + '\n'+ kimnattext + data["kstkimnat"] + '\n' + vydbydunkutext + data["vydbydynok"] + '\n' + stantext +data["stan"]  + '\n' + plbydynku,  reply_markup=plosha_bydunok_kupivlia_inline, parse_mode= ParseMode.HTML)
   
# cina_bydunok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='до 60',callback_data='cinadobydunokkupivlia'),InlineKeyboardButton(text='60 - 120',callback_data='cinamishbydunokkupivliafirst')],
#     [InlineKeyboardButton(text='120-160',callback_data='cinamishbydunokkupivliasecond'),InlineKeyboardButton(text='160-240',callback_data='cinamishbydunokkupivliathird')],
#     [InlineKeyboardButton(text='240-500',callback_data='cinapisliabydunokkupivliafour'),InlineKeyboardButton(text='500-900',callback_data='cinapisliabydunokkupivliafive')],
#     [InlineKeyboardButton(text='900+',callback_data='cinapisliabydunokkupivlias')],
#     [InlineKeyboardButton(text='Назад',callback_data='cinaprevbydunokkupivlia')],
#  ])

@dp.callback_query(F.data=='stepbacklvivandperedmistia_kupivlia')
async def stepbacklvivandperedmistia_kupivlia(callback:CallbackQuery, state:FSMContext):
 
 
    await state.set_state(Kupivlia.typeneruxomist)
    
    data = await state.get_data()

    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"]  + '\n' + typener, reply_markup=type_neruxomist_kupivlia_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='lvivandprlviv')
async def lvivandprlviv(callback:CallbackQuery, state:FSMContext):
    global lvivandperedmistia

    inmarkup = change_lvivandperedmistia_kupivlia(lvivandperedmistia[0][0])
    
    await state.update_data(lvivandperedmistia = form_lviandperedmistia_kupivlia())
    data = await state.get_data()
    pm  = form_lviandperedmistia_kupivlia()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext +pm, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='lvivandprpivnich')
async def lvivandprpivnich(callback:CallbackQuery, state:FSMContext):
    global lvivandperedmistia

    inmarkup = change_lvivandperedmistia_kupivlia(lvivandperedmistia[1][0])
    
    await state.update_data(lvivandperedmistia = form_lviandperedmistia_kupivlia())
    data = await state.get_data()
    pm  = form_lviandperedmistia_kupivlia()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext +pm, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='lvivandprpivden')
async def lvivandprpivden(callback:CallbackQuery, state:FSMContext):
    global lvivandperedmistia

    inmarkup = change_lvivandperedmistia_kupivlia(lvivandperedmistia[2][0])
    
    await state.update_data(lvivandperedmistia = form_lviandperedmistia_kupivlia())
    data = await state.get_data()
    pm  = form_lviandperedmistia_kupivlia()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext +pm, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='lvivandprsaxid')
async def lvivandprsaxid(callback:CallbackQuery, state:FSMContext):
    global lvivandperedmistia

    inmarkup = change_lvivandperedmistia_kupivlia(lvivandperedmistia[3][0])
    
    await state.update_data(lvivandperedmistia = form_lviandperedmistia_kupivlia())
    data = await state.get_data()
    pm  = form_lviandperedmistia_kupivlia()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext +pm, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='lvivandprsxid')
async def lvivandprsxid(callback:CallbackQuery, state:FSMContext):
    global lvivandperedmistia

    inmarkup = change_lvivandperedmistia_kupivlia(lvivandperedmistia[4][0])
    
    await state.update_data(lvivandperedmistia = form_lviandperedmistia_kupivlia())
    data = await state.get_data()
    pm  = form_lviandperedmistia_kupivlia()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ peredmistiatext +pm, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='semliakupivlia')
async def semliakupivlia(callback:CallbackQuery, state:FSMContext):

    await state.set_state(Kupivlia.location)
    await state.update_data(typeneruxomist = 'земля')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=semlialocation_kupivlia_inline, parse_mode= ParseMode.HTML)


#  [InlineKeyboardButton(text='Львів та до обʼїзної',callback_data='lvivdoobj')],
#  [InlineKeyboardButton(text='до 10км від Львова',callback_data='dotenvidlv')],
#  [InlineKeyboardButton(text='10-30 км від Львова',callback_data='mishlviv')],
#  [InlineKeyboardButton(text='30 км і більше від Львова',callback_data='thrirtypislialviv')],
#  [InlineKeyboardButton(text='Назад',callback_data='lvivlocselmlivakupivliastepback'),InlineKeyboardButton(text='Далі',callback_data='lvivlocselmlivakupivliaforward'),]
@dp.callback_query(F.data=='lvivdoobj')
async def lvivdoobj(callback:CallbackQuery, state:FSMContext):

    global loc_semlia_kupivlia
    loc_semlia_kupivlia[0][2] = not loc_semlia_kupivlia[0][2]
    data = await state.get_data()
    loc = form_loc_semlia_kupivlia()
    await state.update_data(location=loc)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=loc_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='dotenvidlv')
async def dotenvidlv(callback:CallbackQuery, state:FSMContext):

    global loc_semlia_kupivlia
    loc_semlia_kupivlia[1][2] = not loc_semlia_kupivlia[1][2]
    data = await state.get_data()
    loc = form_loc_semlia_kupivlia()
    await state.update_data(location=loc)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=loc_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='mishlviv')
async def mishlviv(callback:CallbackQuery, state:FSMContext):

    global loc_semlia_kupivlia
    loc_semlia_kupivlia[2][2] = not loc_semlia_kupivlia[2][2]
    data = await state.get_data()
    loc = form_loc_semlia_kupivlia()
    await state.update_data(location=loc)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=loc_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='thrirtypislialviv')
async def thrirtypislialviv(callback:CallbackQuery, state:FSMContext):

    global loc_semlia_kupivlia
    loc_semlia_kupivlia[3][2] = not loc_semlia_kupivlia[3][2]
    data = await state.get_data()
    loc = form_loc_semlia_kupivlia()
    await state.update_data(location=loc)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=loc_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='lvivlocselmlivakupivliaforward')
async def lvivlocselmlivakupivliaforward(callback:CallbackQuery, state:FSMContext):

    global loc_semlia_kupivlia
    
    data = await state.get_data()
    loc = form_loc_semlia_kupivlia()
    if loc =='':
        loc ='Львів та до обʼїзної, до 10км від Львова, 10-30 км від Львова, 30 км і більше від Львова'
    await state.update_data(location=loc)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc + '\n' + vydvykorystanniaselmliatext , reply_markup=vyd_vykorystannia_semlia_kupivlia_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='lvivlocselmlivakupivliastepback')
async def lvivlocselmlivakupivliaforward(callback:CallbackQuery, state:FSMContext):

    
    data = await state.get_data()

    await state.update_data(location='')
    await state.update_data(typeneruxomist='')
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener , reply_markup=type_neruxomist_kupivlia_inline, parse_mode= ParseMode.HTML)


# vyd_vykorystannia_semlia_kupivlia_pidsabudovu

# vyd_vykorystannia_semlia_kupivlia_obj = [
#     ['під забудову','vyd_vykorystannia_semlia_kupivlia_pidsabudovu',False],
#     ['дачна','vyd_vykorystannia_semlia_kupivlia_dachna',False],
#     ['ОСГ','vyd_vykorystannia_semlia_kupivlia_osg',False],
#     ['промисловість','vyd_vykorystannia_semlia_kupivlia_promyslovist',False],
#     ['торгівля','vyd_vykorystannia_semlia_kupivlia_torgivlia',False],
#     ['торгівля','vyd_vykorystannia_semlia_kupivlia_inshe',False],
# ]

@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_pidsabudovu')
async def vyd_vykorystannia_semlia_kupivlia_pidsabudovu(callback:CallbackQuery, state:FSMContext):

    global vyd_vykorystannia_semlia_kupivlia_obj
    vyd_vykorystannia_semlia_kupivlia_obj[0][2] = not vyd_vykorystannia_semlia_kupivlia_obj[0][2]
    data = await state.get_data()
    vydv = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydv)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydv, reply_markup=vyd_vykorystannia_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_dachna')
async def vyd_vykorystannia_semlia_kupivlia_dachna(callback:CallbackQuery, state:FSMContext):

    global vyd_vykorystannia_semlia_kupivlia_obj
    vyd_vykorystannia_semlia_kupivlia_obj[1][2] = not vyd_vykorystannia_semlia_kupivlia_obj[1][2]
    data = await state.get_data()
    vydv = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydv)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydv, reply_markup=vyd_vykorystannia_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_osg')
async def vyd_vykorystannia_semlia_kupivlia_osg(callback:CallbackQuery, state:FSMContext):

    global vyd_vykorystannia_semlia_kupivlia_obj
    vyd_vykorystannia_semlia_kupivlia_obj[2][2] = not vyd_vykorystannia_semlia_kupivlia_obj[2][2]
    data = await state.get_data()
    vydv = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydv)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydv, reply_markup=vyd_vykorystannia_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_promyslovist')
async def vyd_vykorystannia_semlia_kupivlia_promyslovist(callback:CallbackQuery, state:FSMContext):

    global vyd_vykorystannia_semlia_kupivlia_obj
    vyd_vykorystannia_semlia_kupivlia_obj[3][2] = not vyd_vykorystannia_semlia_kupivlia_obj[3][2]
    data = await state.get_data()
    vydv = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydv)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydv, reply_markup=vyd_vykorystannia_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_torgivlia')
async def vyd_vykorystannia_semlia_kupivlia_torgivlia(callback:CallbackQuery, state:FSMContext):

    global vyd_vykorystannia_semlia_kupivlia_obj
    vyd_vykorystannia_semlia_kupivlia_obj[4][2] = not vyd_vykorystannia_semlia_kupivlia_obj[4][2]
    data = await state.get_data()
    vydv = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydv)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydv, reply_markup=vyd_vykorystannia_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_inshe')
async def vyd_vykorystannia_semlia_kupivlia_inshe(callback:CallbackQuery, state:FSMContext):

    global vyd_vykorystannia_semlia_kupivlia_obj
    vyd_vykorystannia_semlia_kupivlia_obj[5][2] = not vyd_vykorystannia_semlia_kupivlia_obj[5][2]
    data = await state.get_data()
    vydv = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydv)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydv, reply_markup=vyd_vykorystannia_semlia_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='vyd_vykorystannia_semlia_kupivlia_forward')
async def vyd_vykorystannia_semlia_kupivlia_forward(callback:CallbackQuery, state:FSMContext):

    data = await state.get_data()
    vydvyk = form_vyd_vykorystannia_semlia_kupivlia()
    await state.update_data(vydvykorystanniasemlia=vydvyk)
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    nextmarkup,nexttext= check_next_markup(vydvyk,1)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + vydvyk + '\n' + nexttext, reply_markup=nextmarkup, parse_mode= ParseMode.HTML)


# kstsot_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#  [InlineKeyboardButton(text='до 6',callback_data='kstsot_semlia_kupivlia_dosix')],
#  [InlineKeyboardButton(text='6-10',callback_data='kstsot_semlia_kupivlia_sixten')],
#  [InlineKeyboardButton(text='10-20',callback_data='kstsot_semlia_tentwenty')],
#  [InlineKeyboardButton(text='від 20',callback_data='kstsot_semlia_kupivlia_fromtwenty')],
#  [InlineKeyboardButton(text='Назад',callback_data='kstsot_semlia_kupivlia_stepback')],
# ])


@dp.callback_query(F.data=='kstsot_semlia_kupivlia_dosix')
async def kstsot_semlia_kupivlia_dosix(callback:CallbackQuery, state:FSMContext):

    
    kstst = 'до 6'
    await state.update_data(kstsot=kstst)
    data = await state.get_data()

    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    nextmarkup = cina_pidsabudovu_semlia_kupivlia_inline
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + kstst + '\n' + cinatexttysdollar, reply_markup=nextmarkup, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstsot_semlia_kupivlia_sixten')
async def kstsot_semlia_kupivlia_sixten(callback:CallbackQuery, state:FSMContext):

    
    kstst = '6-10'
    await state.update_data(kstsot=kstst)
    data = await state.get_data()

    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    nextmarkup = cina_pidsabudovu_semlia_kupivlia_inline
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + kstst + '\n' + cinatexttysdollar, reply_markup=nextmarkup, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='kstsot_semlia_tentwenty')
async def kstsot_semlia_tentwenty(callback:CallbackQuery, state:FSMContext):

    
    kstst = '10-20'
    await state.update_data(kstsot=kstst)
    data = await state.get_data()

    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    nextmarkup = cina_pidsabudovu_semlia_kupivlia_inline
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + kstst + '\n' + cinatexttysdollar, reply_markup=nextmarkup, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstsot_semlia_kupivlia_fromtwenty')
async def kstsot_semlia_kupivlia_fromtwenty(callback:CallbackQuery, state:FSMContext):

    
    kstst = 'від 20'
    await state.update_data(kstsot=kstst)
    data = await state.get_data()

    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    nextmarkup = cina_pidsabudovu_semlia_kupivlia_inline
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + kstst + '\n' + cinatexttysdollar, reply_markup=nextmarkup, parse_mode= ParseMode.HTML)





# kstga_osg_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#  [InlineKeyboardButton(text='до 1',callback_data='kstga_osg_semlia_kupivlia_doone')],
#  [InlineKeyboardButton(text='1-5',callback_data='kstga_osg_semlia_kupivlia_onefive')],
#  [InlineKeyboardButton(text='5-20',callback_data='kstga_osg_semlia_fivetwenty')],
#  [InlineKeyboardButton(text='20-50',callback_data='kstga_osg_semlia_kupivlia_twentyfifty')],
#  [InlineKeyboardButton(text='50 і більше',callback_data='kstga_osg_semlia_kupivlia_fromfifty')],
#  [InlineKeyboardButton(text='Назад',callback_data='kstga_osg_semlia_kupivlia_stepback')],
# ])



# kstga_prom_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#  [InlineKeyboardButton(text='до 0,5',callback_data='kstga_prom_semlia_kupivlia_dohalf')],
#  [InlineKeyboardButton(text='0,5-1',callback_data='kstga_prom_semlia_kupivlia_halfone')],
#  [InlineKeyboardButton(text='1-3',callback_data='kstga_prom_semlia_onetree')],
#  [InlineKeyboardButton(text='3-10',callback_data='kstga_prom_semlia_kupivlia_treeten')],
#  [InlineKeyboardButton(text='10 і більше',callback_data='kstga_prom_semlia_kupivlia_fromten')],
#  [InlineKeyboardButton(text='Назад',callback_data='kstga_prom_semlia_kupivlia_stepback')],
# ])




@dp.callback_query(F.data=='comment_semlia_kupivliaforward')
async def comment_semlia_kupivliaforward(callback:CallbackQuery, state:FSMContext):
    
    mycoment =''
    await state.update_data(comment=mycoment)
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"], parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"], parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='kstga_prom_semlia_kupivlia_dohalf')
async def kstga_prom_semlia_kupivlia_dohalf(callback:CallbackQuery, state:FSMContext):
    kstga = 'до 0,5'
    await state.update_data(kstgatorgivlia=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstga_prom_semlia_kupivlia_halfone')
async def kstga_prom_semlia_kupivlia_halfone(callback:CallbackQuery, state:FSMContext):
    kstga = '0,5-1'
    await state.update_data(kstgatorgivlia=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstga_prom_semlia_onetree')
async def kstga_prom_semlia_onetree(callback:CallbackQuery, state:FSMContext):
    kstga = '1-3'
    await state.update_data(kstgatorgivlia=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='kstga_prom_semlia_kupivlia_treeten')
async def kstga_prom_semlia_kupivlia_treeten(callback:CallbackQuery, state:FSMContext):
    kstga = '3-10'
    await state.update_data(kstgatorgivlia=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='kstga_prom_semlia_kupivlia_fromten')
async def kstga_prom_semlia_kupivlia_fromten(callback:CallbackQuery, state:FSMContext):
    kstga = '10 і більше'
    await state.update_data(kstgatorgivlia=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='kstga_osg_semlia_kupivlia_doone')
async def kstga_osg_semlia_kupivlia_doone(callback:CallbackQuery, state:FSMContext):
    kstga = 'до 1'
    await state.update_data(kstgaosg=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstga_osg_semlia_kupivlia_onefive')
async def kstga_osg_semlia_kupivlia_onefive(callback:CallbackQuery, state:FSMContext):
    kstga = '1-5'
    await state.update_data(kstgaosg=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstga_osg_semlia_fivetwenty')
async def kstga_osg_semlia_fivetwenty(callback:CallbackQuery, state:FSMContext):
    kstga = '5-20'
    await state.update_data(kstgaosg=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstga_osg_semlia_kupivlia_twentyfifty')
async def kstga_osg_semlia_kupivlia_twentyfifty(callback:CallbackQuery, state:FSMContext):
    kstga = '20-50'
    await state.update_data(kstgaosg=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='kstga_osg_semlia_kupivlia_fromfifty')
async def kstga_osg_semlia_kupivlia_fromfifty(callback:CallbackQuery, state:FSMContext):
    kstga = '50 і більше'
    await state.update_data(kstgaosg=kstga)
    data = await state.get_data()
    await callback.message.answer(text= 'Ваш фільтр======>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstgatext+ kstga , parse_mode= ParseMode.HTML)

# cina_pidsabudovu_semlia_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#  [InlineKeyboardButton(text='до 15',callback_data='cina_pidsabudovu_semlia_kupivlia_dofifteen')],
#  [InlineKeyboardButton(text='15-30',callback_data='cina_pidsabudovu_semlia_kupivlia_fifteenthirty')],
#  [InlineKeyboardButton(text='30-60',callback_data='cina_pidsabudovu_semlia_thirtysixty')],
#  [InlineKeyboardButton(text='60-120',callback_data='cina_pidsabudovu_semlia_kupivlia_sixtyhundredtwenty')],
#  [InlineKeyboardButton(text='120 і більше',callback_data='cina_pidsabudovu_semlia_kupivlia_fromhundredtwenty')],
#  [InlineKeyboardButton(text='Назад',callback_data='cina_pidsabudovu_semlia_kupivlia_stepback'),InlineKeyboardButton(text='Далі',callback_data='cina_pidsabudovu_semlia_kupivlia_forward')],
# ])


@dp.callback_query(F.data=='cina_pidsabudovu_semlia_kupivlia_dofifteen')
async def cina_pidsabudovu_semlia_kupivlia_dofifteen(callback:CallbackQuery, state:FSMContext):
    cnsm = 'до 15'
    await state.update_data(cinasemliakupivlia=cnsm)
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр====>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='cina_pidsabudovu_semlia_kupivlia_fifteenthirty')
async def cina_pidsabudovu_semlia_kupivlia_fifteenthirty(callback:CallbackQuery, state:FSMContext):
    cnsm = '15-30'
    await state.update_data(cinasemliakupivlia=cnsm)
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр====>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cina_pidsabudovu_semlia_thirtysixty')
async def cina_pidsabudovu_semlia_thirtysixty(callback:CallbackQuery, state:FSMContext):
    cnsm = '30-60'
    await state.update_data(cinasemliakupivlia=cnsm)
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр====>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='cina_pidsabudovu_semlia_kupivlia_sixtyhundredtwenty')
async def cina_pidsabudovu_semlia_kupivlia_sixtyhundredtwenty(callback:CallbackQuery, state:FSMContext):
    cnsm = '60-120'
    await state.update_data(cinasemliakupivlia=cnsm)
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр====>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cina_pidsabudovu_semlia_kupivlia_fromhundredtwenty')
async def cina_pidsabudovu_semlia_kupivlia_fromhundredtwenty(callback:CallbackQuery, state:FSMContext):
    cnsm = '120 і більше'
    await state.update_data(cinasemliakupivlia=cnsm)
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)
    await callback.message.answer(text= 'Ваш фільтр====>'+'\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + data["location"] + '\n' + vydvykorystanniaselmliatext + data["vydvykorystanniasemlia"] + '\n' + kstsottext + data["kstsot"] + '\n' + cinatexttysdollar + cnsm, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='komerciakupivlia')
async def komerciakupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global rayon_checked_start_kupivlia
    rayon_checked_kupivlia = copy.deepcopy( rayon_checked_start_kupivlia)
    inmarkup = change_rayon_kupivlia('start')
    await state.set_state(Kupivlia.typeneruxomist)
    await state.update_data(typeneruxomist = 'комерція')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='carplacekupivlia')
async def carplacekupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global rayon_checked_start_kupivlia
    rayon_checked_kupivlia = copy.deepcopy( rayon_checked_start_kupivlia)
    inmarkup = change_rayon_kupivlia('start')
    await state.set_state(Kupivlia.typeneruxomist)
    await state.update_data(typeneruxomist = 'машиномісце')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] +'\n'+ locationtext + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


 #keyboard.append([InlineKeyboardButton(text='Назад',callback_data='stepbackrayonskupivlia'),InlineKeyboardButton(text='Далі',callback_data='stepforwardrayonskupivlia')],)

@dp.callback_query(F.data=='stepbackrayonskupivlia')
async def stepbackrayonskupivlia(callback:CallbackQuery, state:FSMContext):
 
    await state.set_state(Kupivlia.typeneruxomist)
    await state.update_data(typeneruxomist='')
    data = await state.get_data()
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["kupivlia"] + '\n' + typener + data['typeneruxomist'], reply_markup=type_neruxomist_kupivlia_inline, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='stepforwardrayonskupivlia')
async def stepforwardrayonskupivlia(callback:CallbackQuery, state:FSMContext):
        global rayon_checked_kupivlia
        global change_rayon_kupivlia

        if rayon_checked_kupivlia[0][1]==False and rayon_checked_kupivlia[0][4]==False and rayon_checked_kupivlia[1][1]==False and rayon_checked_kupivlia[1][4]==False and rayon_checked_kupivlia[2][1]==False and rayon_checked_kupivlia[2][4]==False:

            change_rayon_kupivlia('all')
    
    
        inmarkup = type_neruxomist_kupivlia_inline
        await state.set_state(Kupivlia.location)

        await state.update_data(location =  form_rayonlist_kupivlia())
        data = await state.get_data()
        #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
        loc = form_rayonlist_kupivlia()
        # await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
        

        if data['typeneruxomist']=='кімната':
            await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc + '\n' +  cinatextdollar, reply_markup=cina_kimnata_kupivlia_inline, parse_mode= ParseMode.HTML)
        elif data['typeneruxomist']=='квартира':
            inmarkup = change_kst_kupivlia('start')
            await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc + '\n' +kimnattext , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
        elif data['typeneruxomist']=='будинок':
            inmarkup = change_kst_kupivlia('start')
            await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc + '\n' +kimnattext , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
        elif data['typeneruxomist']=='комерція':
            await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc + '\n' +vyd_vykorystanniatext , reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
        elif data['typeneruxomist']=='машиномісце':
            await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc + '\n' +vyd_parkomisce , reply_markup=vyd_mashynomisce_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='galickiykupivlia')
async def galickiykupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia(rayon_checked_kupivlia[0][0])
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())
    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc,reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='frankivskijkupivlia')
async def frankivskijkupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia(rayon_checked_kupivlia[0][3])
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())
    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + loc,reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='shevchenkivskijkupivlia')
async def shevchenkivskijkupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia(rayon_checked_kupivlia[1][0])
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())
    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='syxivskijkupivlia')
async def syxivskijkupivlia( callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia(rayon_checked_kupivlia[1][3])
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())
    
    data = await state.get_data()
    loc = form_rayonlist_kupivlia()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    #await callback.message.edit_caption(caption= "_"+'\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"], reply_markup=InlineKeyboardMarkup(inline_keyboard=change_rayon_kupivlia(rayon_checked_kupivlia[1][3])), parse_mode= ParseMode.HTML)
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='lychakivskijkupivlia')
async def lychakivskijkupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia(rayon_checked_kupivlia[2][0])
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())
    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"], reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='salisnichnijkupivlia')
async def salisnichnijkupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia(rayon_checked_kupivlia[2][3])
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())

    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"],reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
 
 
@dp.callback_query(F.data=='selectallrayonskupivlia')
async def selectallrayonskupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia('all')
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())

    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch + data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + data["location"],reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


# cina_kimnata_kupivlia_inline  = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='до 12000',callback_data='cinadokimantakupivlia')],
#     [InlineKeyboardButton(text='12000-18000',callback_data='cinamishkimantakupivlia')],
#     [InlineKeyboardButton(text='18000',callback_data='cinapisliakimantakupivlia')],
     
#     [InlineKeyboardButton(text='Назад',callback_data='cinaprevkimantakupivlia')],
#  ])

@dp.callback_query(F.data=='cinadokimantakupivlia')
async def cinadokimantakupivlia(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakupivlia)
    await state.update_data(cinakupivlia = 'до 12000')

    data = await state.get_data()
    ctd = 'до 12000'
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch + data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + data["location"] +  '\n' + cinatextdollar + ctd, reply_markup=cina_kimnata_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + data["location"] + '\n' + cinatextdollar + ctd, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='cinamishkimantakupivlia')
async def cinamishkimantakupivlia(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakupivlia)
    await state.update_data(cinakupivlia = '12000-18000')

    data = await state.get_data()
    ctd = '12000-18000'
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch + data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + data["location"] +  '\n' + cinatextdollar + ctd, reply_markup=cina_kimnata_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + data["location"] + '\n' + cinatextdollar + ctd, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='cinapisliakimantakupivlia')
async def cinapisliakimantakupivlia(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakupivlia)
    await state.update_data(cinakupivlia = '18000')

    data = await state.get_data()
    ctd = '18000'
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch + data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + data["location"] +  '\n' + cinatextdollar + ctd, reply_markup=cina_kimnata_kupivlia_inline, parse_mode= ParseMode.HTML)
    await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' + data["location"] +  '\n' + cinatextdollar + ctd, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinaprevkimantakupivlia')
async def cinaprevkimantakupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia('start')
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = form_rayonlist_kupivlia())
    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='k1kupivlia')
async def k1kupivlia(callback:CallbackQuery, state:FSMContext):

    global kst_checked_kupivlia
    global change_kst_kupivlia
    inmarkup = change_kst_kupivlia("1k")
    await state.set_state(Kupivlia.kstkimnat)
    await state.update_data(kstkimnat = form_kstlist_kupivlia())
    data = await state.get_data()
    ksttextvalue = form_kstlist_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='k2kupivlia')
async def k2kupivlia(callback:CallbackQuery, state:FSMContext):

    global kst_checked_kupivlia
    global change_kst_kupivlia
    inmarkup = change_kst_kupivlia("2k")
    await state.set_state(Kupivlia.kstkimnat)
    await state.update_data(kstkimnat = form_kstlist_kupivlia())
    data = await state.get_data()
    ksttextvalue = form_kstlist_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='k3kupivlia')
async def k3kupivlia(callback:CallbackQuery, state:FSMContext):

    global kst_checked_kupivlia
    global change_kst_kupivlia
    inmarkup = change_kst_kupivlia("3k")
    await state.set_state(Kupivlia.kstkimnat)
    await state.update_data(kstkimnat = form_kstlist_kupivlia())
    data = await state.get_data()
    ksttextvalue = form_kstlist_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='k4kupivlia')
async def k4kupivlia(callback:CallbackQuery, state:FSMContext):

    global kst_checked_kupivlia
    global change_kst_kupivlia
    inmarkup = change_kst_kupivlia("4k")
    await state.set_state(Kupivlia.kstkimnat)
    await state.update_data(kstkimnat = form_kstlist_kupivlia())
    data = await state.get_data()
    ksttextvalue = form_kstlist_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


#   keyboard.append([InlineKeyboardButton(text='Назад',callback_data='kststepback_kupivlia'),InlineKeyboardButton(text='Далі',callback_data='kstnext_kupivlia')],)
@dp.callback_query(F.data=='kstnext_kupivlia')
async def kstnext_kupivlia(callback:CallbackQuery, state:FSMContext):
    global kst_checked_kupivlia
    global change_kst_kupivlia
    await state.set_state(Kupivlia.typebydynok)
    if kst_checked_kupivlia[0][1]==False and kst_checked_kupivlia[0][3]==False and kst_checked_kupivlia[1][1]==False and kst_checked_kupivlia[1][3] == False:
        change_kst_kupivlia('all')

    await state.update_data(kstkimnat = form_kstlist_kupivlia())
    data = await state.get_data()
    ksttextvalue = form_kstlist_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  data['location'] + '\n' +  kimnattext + ksttextvalue + '\n' + typebydynoktext , reply_markup=type_bydynok_kupivlia_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kststepback_kupivlia')
async def k4kupivlia(callback:CallbackQuery, state:FSMContext):
    global rayon_checked_kupivlia
    global change_rayon_kupivlia
    inmarkup = change_rayon_kupivlia('start')
    await state.set_state(Kupivlia.location)
    
    await state.update_data(location = '')
    data = await state.get_data()
    #await callback.message.edit_text( data["kupivlia"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = ''
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  '\n' + loc + '\n' +  kimnattext, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)




# type_bydynok_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='будується',callback_data='bydyetsia'),InlineKeyboardButton(text='новобудова',callback_data='novobydova')],
#     [InlineKeyboardButton(text='українська забудова > 10 років',callback_data='ukrten')],
#     [InlineKeyboardButton(text='радянська забудова',callback_data='radianska')],
#     [InlineKeyboardButton(text='будинок старого Львова',callback_data='stariylviv')],
#     [InlineKeyboardButton(text='Назад',callback_data='typebydynokstepback')],
    
#  ])

@dp.callback_query(F.data=='bydyetsia')
async def bydyetsia(callback:CallbackQuery, state:FSMContext):
    global type_bydynok_kupivlia
    type_bydynok_kupivlia[0][2] = not type_bydynok_kupivlia[0][2]
    await state.set_state(Kupivlia.typebydynok)
    
    data = await state.get_data()
    await state.update_data(typebydynok =  form_type_bydynok_kupivlia())
    tb = form_type_bydynok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  data['location'] +'\n' +  kimnattext + data["kstkimnat"] + '\n' + typebydynoktext + tb, reply_markup=type_bydynok_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='novobydova')
async def novobydova(callback:CallbackQuery, state:FSMContext):
    global type_bydynok_kupivlia
    type_bydynok_kupivlia[1][2] = not type_bydynok_kupivlia[1][2]
    await state.set_state(Kupivlia.typebydynok)
    
    data = await state.get_data()
    await state.update_data(typebydynok = form_type_bydynok_kupivlia())
    tb = form_type_bydynok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  data['location'] +'\n' +  kimnattext + data["kstkimnat"] + '\n' + typebydynoktext + tb , reply_markup=type_bydynok_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='ukrten')
async def ukrten(callback:CallbackQuery, state:FSMContext):
    global type_bydynok_kupivlia
    type_bydynok_kupivlia[2][2] = not type_bydynok_kupivlia[2][2]
    await state.set_state(Kupivlia.typebydynok)
    data = await state.get_data()
    await state.update_data(typebydynok = form_type_bydynok_kupivlia())
    tb = form_type_bydynok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  data['location'] +'\n' +  kimnattext + data["kstkimnat"] + '\n' + typebydynoktext + tb , reply_markup=type_bydynok_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='radianska')
async def radianska(callback:CallbackQuery, state:FSMContext):
    global type_bydynok_kupivlia
    type_bydynok_kupivlia[3][2] = not type_bydynok_kupivlia[3][2]
    await state.set_state(Kupivlia.typebydynok)
    data = await state.get_data()
    await state.update_data(typebydynok =  form_type_bydynok_kupivlia())
    tb = form_type_bydynok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  data['location'] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + typebydynoktext + tb , reply_markup=type_bydynok_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='stariylviv')
async def stariylviv(callback:CallbackQuery, state:FSMContext):
    global type_bydynok_kupivlia
    type_bydynok_kupivlia[4][2] = not type_bydynok_kupivlia[4][2]
    await state.set_state(Kupivlia.typebydynok)
    data = await state.get_data()
    await state.update_data(typebydynok =  form_type_bydynok_kupivlia())
    tb = form_type_bydynok_kupivlia()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext +  data['location'] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + typebydynoktext + tb , reply_markup=type_bydynok_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='typebydynokstepback')
async def typebydynokstepback(callback:CallbackQuery, state:FSMContext):
    global kst_checked_kupivlia
    global change_kst_kupivlia
    inmarkup = change_kst_kupivlia('start')
    await state.set_state(Kupivlia.kstkimnat)
    await state.update_data(typebydynok =  '')

    data = await state.get_data()
    ksttextvalue = ''
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='typebydynokforward')
async def typebydynokforward(callback:CallbackQuery, state:FSMContext):
    global type_bydynok_kupivlia
    if type_bydynok_kupivlia[0][2] == False and type_bydynok_kupivlia[1][2] == False and type_bydynok_kupivlia[2][2] == False and type_bydynok_kupivlia[3][2]  == False and type_bydynok_kupivlia[4][2] == False:
        type_bydynok_kupivlia[0][2] = True 
        type_bydynok_kupivlia[1][2] = True
        type_bydynok_kupivlia[2][2] = True
        type_bydynok_kupivlia[3][2] = True
        type_bydynok_kupivlia[4][2] = True
    await state.update_data(typebydynok =form_type_bydynok_kupivlia())
    await state.set_state(Kupivlia.stan)
    
    data = await state.get_data()
    tb = form_type_bydynok_kupivlia()

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + data["kstkimnat"] + '\n' +typebydynoktext + data["typebydynok"] +'\n' + stantext, reply_markup=stan_kupivlia_inline, parse_mode= ParseMode.HTML)

#type_bydynok_kupivlia_inline




# stan_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='новий ремонт',callback_data='novyiremont')],
#     [InlineKeyboardButton(text='хороший житловий',callback_data='xoroshiyshitloviy')],
#     [InlineKeyboardButton(text='без ремонту',callback_data='besremontu')],
#     [InlineKeyboardButton(text='від забудовника',callback_data='vidsabudovnyka')],

#     [InlineKeyboardButton(text='Назад',callback_data='stanstepback'),InlineKeyboardButton(text='Назад',callback_data='stanstepforward')],
    
#  ])

@dp.callback_query(F.data=='novyiremont')
async def novyiremont(callback:CallbackQuery, state:FSMContext):
  
    global stan_kupivlia
    stan_kupivlia[0][2] = not stan_kupivlia[0][2]
    data = await state.get_data()
    await state.update_data(stan = form_stan_kupivlia())

    st = form_stan_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext + st, reply_markup=stan_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='xoroshiyshitloviy')
async def xoroshiyshitloviy(callback:CallbackQuery, state:FSMContext):
    global stan_kupivlia
    stan_kupivlia[1][2] = not stan_kupivlia[1][2]
    await state.update_data(stan = form_stan_kupivlia())
    st = form_stan_kupivlia()
    data = await state.get_data()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext + st , reply_markup=stan_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='besremontu')
async def besremontu(callback:CallbackQuery, state:FSMContext):

    global stan_kupivlia
    stan_kupivlia[2][2] = not stan_kupivlia[2][2]    
    data = await state.get_data()
    await state.update_data(stan = form_stan_kupivlia())
    st = form_stan_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext + st , reply_markup=stan_kupivlia_keyboard(), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='vidsabudovnyka')
async def vidsabudovnyka(callback:CallbackQuery, state:FSMContext):
    global stan_kupivlia
    stan_kupivlia[3][2] = not stan_kupivlia[3][2]  
    data = await state.get_data()
    await state.update_data(stan = form_stan_kupivlia())
    st = form_stan_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext + st, reply_markup=stan_kupivlia_keyboard(), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='stanstepforward')
async def stanstepforward(callback:CallbackQuery, state:FSMContext):
    global stan_kupivlia
    if stan_kupivlia[0][2] == False and stan_kupivlia[1][2] == False and stan_kupivlia[2][2] == False and stan_kupivlia[3][2] == False:
        stan_kupivlia[0][2] = True
        stan_kupivlia[1][2] = True
        stan_kupivlia[2][2] = True
        stan_kupivlia[3][2] = True
    data = await state.get_data()
    await state.update_data(stan = form_stan_kupivlia())
    st = form_stan_kupivlia()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext + st + '\n' + plkvartyry, reply_markup=plosha_kvartyry_kupivlia_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='stanstepback')
async def stanstepback(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.typebydynok)
    data = await state.get_data()
    await state.update_data(stan = '')
    st = ''
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext , reply_markup=type_bydynok_kupivlia_inline, parse_mode= ParseMode.HTML) 
# stanstepback

# plosha_kvartyry_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='до 30',callback_data='ploshado'),InlineKeyboardButton(text='30-55',callback_data='ploshamishfirst')],
#     [InlineKeyboardButton(text='55-75',callback_data='ploshamishsecond'),InlineKeyboardButton(text='75-100',callback_data='ploshamishthird')],
#     [InlineKeyboardButton(text='100-150',callback_data='ploshamishfour'), InlineKeyboardButton(text='150 і більше',callback_data='ploshapislia')],


#     [InlineKeyboardButton(text='Назад',callback_data='ploshastepback')],
    
#  ])
@dp.callback_query(F.data=='ploshado')
async def ploshado(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = 'до 30')
    pl = 'до 30'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + pl+ '\n' + '\n' + '🦁'+commenttextadv, reply_markup=comment_inline, parse_mode= ParseMode.HTML) 


@dp.callback_query(F.data=='ploshamishfirst')
async def ploshamishfirst(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = '30-55')
    pl = '30-55'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + pl+ '\n' + '\n' + '🦁'+commenttextadv, reply_markup=comment_inline, parse_mode= ParseMode.HTML) 

@dp.callback_query(F.data=='ploshamishsecond')
async def ploshamishsecond(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = '55-75')
    pl = '55-75'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + pl+ '\n' + '\n' + '🦁'+commenttextadv, reply_markup=comment_inline, parse_mode= ParseMode.HTML) 

@dp.callback_query(F.data=='ploshamishthird')
async def ploshamishthird(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = '75-100')
    pl = '75-100'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + pl+ '\n' +  '\n' +'🦁'+commenttextadv, reply_markup=comment_inline, parse_mode= ParseMode.HTML) 

@dp.callback_query(F.data=='ploshamishfour')
async def ploshamishfour(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = '100-150')
    pl = '100-150'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + pl+ '\n' + '\n' +'🦁'+commenttextadv, reply_markup=comment_inline, parse_mode= ParseMode.HTML) 


@dp.callback_query(F.data=='ploshapislia')
async def ploshapislia(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = '150 і більше')
    pl = '150 і більше'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + pl + '\n' + '\n' + '🦁'+commenttextadv, reply_markup=comment_inline, parse_mode= ParseMode.HTML) 

@dp.callback_query(F.data=='ploshastepback')
async def ploshastepback(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.stan)
    data = await state.get_data()
    await state.update_data(stan = '')
    st = ''
    
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext, reply_markup=stan_kupivlia_inline, parse_mode= ParseMode.HTML) 

#  [InlineKeyboardButton(text='Назад',callback_data='commentstepback'),InlineKeyboardButton(text='Далі',callback_data='commentforward')],

@dp.callback_query(F.data=='commentstepback')
async def commentstepback(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.ploshakvartyry)
    data = await state.get_data()
    await state.update_data(ploshakvartyry = '')
    pl = ''
    
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' + stantext + data["stan"] +  '\n' + plkvartyry, reply_markup=plosha_kvartyry_kupivlia_inline, parse_mode= ParseMode.HTML) 


@dp.callback_query(F.data=='commentforward')
async def commentforward(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    data = await state.get_data()
    #getcomment
    await state.update_data(comment = '')
    com = 'Ваш коментар'
    
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + '\n'+ "🦁 <i><b>"+ cinatexttysdollar +"</b></i>❔", reply_markup=cina_kvartyra_kupivlia_inline, parse_mode= ParseMode.HTML) 

# cina_kvartyra_kupivlia_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='до 30',callback_data='cinakvartyrakupivliado'),InlineKeyboardButton(text='30-50',callback_data='cinakvartyrakupivliamishfirst')],
#     [InlineKeyboardButton(text='50-70',callback_data='cinakvartyrakupivliamishsecond'),InlineKeyboardButton(text='70-100',callback_data='cinakvartyrakupivliamishthird')],
#     [InlineKeyboardButton(text='100-140',callback_data='cinakvartyrakupivliamishfour'),InlineKeyboardButton(text='140-180',callback_data='cinakvartyrakupivliamishfifth')],
#     [InlineKeyboardButton(text='180-250',callback_data='cinakvartyrakupivliamishsix'),InlineKeyboardButton(text='250+',callback_data='cinakvartyrakupivliapislia')],
#     [InlineKeyboardButton(text='Назад',callback_data='cinakvartyrakupivliastepback')],
    
#  ])

@dp.callback_query(F.data=='cinakvartyrakupivliado')
async def cinakvartyrakupivliado(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = 'до 30')
    data = await state.get_data()
    #getcomment
    
    ckv = 'до 30'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)
    
    await showObjectsByFilter(data,callback)


@dp.callback_query(F.data=='cinakvartyrakupivliamishfirst')
async def cinakvartyrakupivliamishfirst(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '30-50')
    data = await state.get_data()
    #getcomment
    
    ckv = '30-50'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)

@dp.callback_query(F.data=='cinakvartyrakupivliamishsecond')
async def cinakvartyrakupivliamishsecond(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '50-70')
    data = await state.get_data()

    ckv = '50-70'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)

@dp.callback_query(F.data=='cinakvartyrakupivliamishthird')
async def cinakvartyrakupivliamishthird(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '70-100')
    data = await state.get_data()
    ckv = '70-100'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)

@dp.callback_query(F.data=='cinakvartyrakupivliamishfour')
async def cinakvartyrakupivliamishfour(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '100-140')
    data = await state.get_data()
    ckv = '100-140'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)

@dp.callback_query(F.data=='cinakvartyrakupivliamishfifth')
async def cinakvartyrakupivliamishfifth(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '140-180')
    data = await state.get_data()
    ckv = '140-180'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)

@dp.callback_query(F.data=='cinakvartyrakupivliamishsix')
async def cinakvartyrakupivliamishsix(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '180-250')
    data = await state.get_data()
    #getcomment
    
    ckv = '180-250'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''

    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)

@dp.callback_query(F.data=='cinakvartyrakupivliapislia')
async def cinakvartyrakupivliapislia(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.cinakvartyrakupivlia)
    await state.update_data(cinakvartyrakupivlia = '250+')
    data = await state.get_data()
    #getcomment
    
    ckv = '250+'
    if data["comment"]!='':
        com = data["comment"]
    else:
        com = ''
    text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv
    savefilter(True,str(data["user"].from_user.id), text, data)
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] + '\n' + commenttext +  com + '\n' + cinatexttysdollar +ckv,  reply_markup=filter_end, parse_mode= ParseMode.HTML) 
    


@dp.callback_query(F.data=='cinakvartyrakupivliastepback')
async def cinakvartyrakupivliado(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Kupivlia.comment)
    data = await state.get_data()
    #getcomment
    await state.update_data(comment = '')

    com = 'Ваш коментар'
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["kupivlia"] + '\n' + typener + data["typeneruxomist"] + '\n' + locationtext + '\n' +  data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' +  typebydynoktext + data["typebydynok"] + '\n' +  stantext + data["stan"] + '\n' + plkvartyry + data["ploshakvartyry"] +  '\n' + commenttext  ,  reply_markup=comment_inline, parse_mode= ParseMode.HTML) 
    


@dp.callback_query(F.data=='terminorendunext')
async def terminorendunext(callback:CallbackQuery, state:FSMContext):
    pass

@dp.callback_query(F.data=='kimnatastepback')
async def kimnatastepback(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    global kst_checked_start
    global kst_checked
    data = await state.get_data()
    if data['typeneruxomist'] == 'кімната':
        rayon_checked = copy.deepcopy( rayon_checked_start)
        inmarkup = change_rayon('start')
        await state.set_state(Orenda.location)
        await state.update_data(location = '')
    
        loc = form_rayonlist()
        #inline_message_id= str(data["user"].caption), 
        #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
        await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    elif data['typeneruxomist'] == 'квартира' or data['typeneruxomist'] == 'будинок':
        kst_checked = copy.deepcopy( kst_checked_start)
        inmarkup = change_kst('start')
        await state.set_state(Orenda.kstkimnat)
        await state.update_data(kstkimnat = '')
    
        ksttext= form_kstlist()
        #inline_message_id= str(data["user"].caption), 
        #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
        await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + data["location"] +'\n'+ kimnattext, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='stepback')
async def stepback(callback:CallbackQuery, state:FSMContext):
    await state.set_state(User.user)
    data = await state.get_data()
    #await state.set_state(Orenda.orenda)
    await callback.message.edit_caption(caption=f'<a href="tg://user?id={data["user"].from_user.id}">{data["user"].from_user.first_name}</a>'+ ' ' + 'Ви хочете                                            .', reply_markup=mmenuinline,  parse_mode=ParseMode.HTML)
    
@dp.callback_query(F.data=='stepbackkupivlia')
async def stepback(callback:CallbackQuery, state:FSMContext):
    await state.set_state(User.user)
    data = await state.get_data()
    #await state.set_state(Orenda.orenda)
    await callback.message.edit_caption(caption=f'<a href="tg://user?id={data["user"].from_user.id}">{data["user"].from_user.first_name}</a>'+ ' ' + 'Ви хочете                                            .', reply_markup=mmenuinline,  parse_mode=ParseMode.HTML)

#   ["Галицький",False,"galickiy","Франківський",False,"frankivskij"],
#                      ["Шевченківський",False,"shevchenkivskij","Сихівський",False,"syxivskij"],
#                      ["Личаківський",False,"lychakivskij","Залізничний",False,"salisnichnij"],
@dp.callback_query(F.data=='galickiy')
async def galickiy(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon(rayon_checked[0][0])
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc,reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='frankivskij')
async def frankivskij(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon(rayon_checked[0][3])
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik +  '\n' + loc,reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='shevchenkivskij')
async def shevchenkivskij(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon(rayon_checked[1][0])
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='syxivskij')
async def syxivskij( callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon(rayon_checked[1][3])
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())
    
    data = await state.get_data()
    loc = form_rayonlist()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    #await callback.message.edit_caption(caption= "_"+'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"], reply_markup=InlineKeyboardMarkup(inline_keyboard=change_rayon(rayon_checked[1][3])), parse_mode= ParseMode.HTML)
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='lychakivskij')
async def lychakivskij(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon(rayon_checked[2][0])
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    await callback.message.edit_caption(caption= '\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"], reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='salisnichnij')
async def salisnichnij(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon(rayon_checked[2][3])
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())

    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"],reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
 
 
@dp.callback_query(F.data=='selectallrayons')
async def selectallrayons(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon
    inmarkup = change_rayon('all')
    await state.set_state(Orenda.location)
    
    await state.update_data(location = form_rayonlist())

    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch + data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik +  '\n' + data["location"],reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    



@dp.callback_query(F.data=='stepforwardrayons')
async def stepforwardrayons(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global change_rayon

    if rayon_checked[0][1]==False and rayon_checked[0][4]==False and rayon_checked[1][1]==False and rayon_checked[1][4]==False and rayon_checked[2][1]==False and rayon_checked[2][4]==False:
        rayon_checked[0][1]=True
        rayon_checked[0][4]=True
        rayon_checked[1][1]=True
        rayon_checked[1][4]=True
        rayon_checked[2][1]=True
        rayon_checked[2][4]=True
        change_rayon('all')
   
   
    inmarkup = type_neruxomist_inline
    await state.set_state(Orenda.location)

    await state.update_data(location =  form_rayonlist())
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    loc = form_rayonlist()
    # await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    await state.set_state(Orenda.terminorendu)
    await state.update_data(terminorendu =  'Не задано')
    if data['typeneruxomist']=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc + '\n' +termin , reply_markup=terminorendu_inline, parse_mode= ParseMode.HTML)
    elif data['typeneruxomist']=='квартира' or data['typeneruxomist']=='будинок':
        inmarkup = change_kst('start')
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc + '\n' +kimnattext , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)
    elif data['typeneruxomist']=='комерція':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc + '\n' +vyd_vykorystanniatext , reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
    elif data['typeneruxomist']=='машиномісце':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + loc + '\n' +vyd_parkomisce , reply_markup=vyd_mashynomisce_inline, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='stepbackrayons')
async def stepbackrayons(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    await state.set_state(Orenda.typeneruxomist)
   
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    
    await callback.message.edit_caption(caption=  '\n'+ '\n'+ wesearch + data["orenda"], reply_markup=type_neruxomist_inline, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data=='kststepback')
async def kststepback(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.location)
   
    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode=ParseMode.HTML)



@dp.callback_query(F.data=='k1')
async def k1(callback:CallbackQuery, state:FSMContext):

    global kst_checked
    global change_kst
    inmarkup = change_kst("1k")
    await state.set_state(Orenda.kstkimnat)
    
    await state.update_data(kstkimnat = form_kstlist())

    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    ksttextvalue = form_kstlist()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='k2')
async def k2(callback:CallbackQuery, state:FSMContext):

    global kst_checked
    global change_kst
    inmarkup = change_kst("2k")
    await state.set_state(Orenda.kstkimnat)
    
    await state.update_data(kstkimnat = form_kstlist())

    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    ksttextvalue = form_kstlist()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='k3')
async def k3(callback:CallbackQuery, state:FSMContext):

    global kst_checked
    global change_kst
    inmarkup = change_kst("3k")
    await state.set_state(Orenda.kstkimnat)
    
    await state.update_data(kstkimnat = form_kstlist())

    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    ksttextvalue = form_kstlist()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"] + '\n' + '\n' +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='k4')
async def k4(callback:CallbackQuery, state:FSMContext):

    global kst_checked
    global change_kst
    inmarkup = change_kst("4k")
    await state.set_state(Orenda.kstkimnat)
    
    await state.update_data(kstkimnat = form_kstlist())

    data = await state.get_data()
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    ksttextvalue = form_kstlist()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"] + '\n'  +  kimnattext + ksttextvalue, reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='kstnext')
async def kstnext(callback:CallbackQuery, state:FSMContext):
    global kst_checked
    global change_kst
    if kst_checked[0][1]==False and kst_checked[0][3]==False and kst_checked[1][1]==False and kst_checked[1][3]==False:
        change_kst('all')
    inmarkup = terminorendu_inline
   
    await state.set_state(Orenda.kstkimnat)
    await state.update_data(kstkimnat = form_kstlist())

    data = await state.get_data()
    ksttextvalue = form_kstlist()
    await callback.message.edit_caption(caption='\n'+ '\n' + wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' +  data["location"] + '\n'  +  kimnattext + ksttextvalue + '\n' + termin, reply_markup=terminorendu_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='termnext')
async def termnext(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()

     if data["typeneruxomist"]=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)
     elif data["typeneruxomist"]=='квартира' or data["typeneruxomist"]=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML) 
     
     await state.set_state(Orenda.tvaryny)

@dp.callback_query(F.data=='dotermin')
async def dotermin(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(terminorendu = 'До 3-х місяців')
     to= 'До 3-х місяців'
     if data["typeneruxomist"]=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + to + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)
     elif data["typeneruxomist"]=='квартира' or data["typeneruxomist"]=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + to + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML) 
     await state.set_state(Orenda.tvaryny)


@dp.callback_query(F.data=='terminmish')
async def terminmish(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(terminorendu = '3-6 місяців')
     to= '3-6 місяців'
     if data["typeneruxomist"]=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + to + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)
     elif data["typeneruxomist"]=='квартира' or data["typeneruxomist"]=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + to + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML) 
     await state.set_state(Orenda.tvaryny)


@dp.callback_query(F.data=='terminpislia')
async def terminpislia(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(terminorendu = 'від 6 місяців')
     to= 'від 6 місяців'
     if data["typeneruxomist"]=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + to + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)
     elif data["typeneruxomist"]=='квартира' or data["typeneruxomist"]=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + to + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML) 
     await state.set_state(Orenda.tvaryny)



@dp.callback_query(F.data=='tvarynytak')
async def tvarynytak(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(tvaryny = 'Так')
     tvr = 'Так'
     if data['typeneruxomist']=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_inline, parse_mode= ParseMode.HTML)
     elif data['typeneruxomist']=='квартира':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_kvartyra_inline, parse_mode= ParseMode.HTML) 
     elif data['typeneruxomist']=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)    
     elif data['typeneruxomist']=='машиномісце':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)    
     await state.set_state(Orenda.cina)

@dp.callback_query(F.data=='tvarynyni')
async def tvarynyni(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(tvaryny = 'Ні')
     tvr = 'Ні'
     if data['typeneruxomist']=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_inline, parse_mode= ParseMode.HTML)
     elif data['typeneruxomist']=='квартира':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_kvartyra_inline, parse_mode= ParseMode.HTML) 
     elif data['typeneruxomist']=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)    
     elif data['typeneruxomist']=='машиномісце':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr + '\n' +cinatext, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)    

@dp.callback_query(F.data=='tvarynyprev')
async def tvarynyprev(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(tvaryny = '')
     tvr = ''
     to = ''
     if data['typeneruxomist']=='кімната':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + to , reply_markup=terminorendu_inline, parse_mode= ParseMode.HTML)
     elif data['typeneruxomist']=='квартира':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin, reply_markup=terminorendu_inline, parse_mode= ParseMode.HTML) 
     elif data['typeneruxomist']=='будинок':
        await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin, reply_markup=terminorendu_inline, parse_mode= ParseMode.HTML)    
     await state.set_state(Orenda.terminorendu)
 

@dp.callback_query(F.data=='cinado')
async def cinado(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = 'До 3500')
     cn = 'До 3500'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinamish')
async def cinamish(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = '3500-5500')
     cn = '3500-5500'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinapislia')
async def cinapislia(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = 'від 5500')
     cn = 'від 5500'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)



@dp.callback_query(F.data=='cinaprev')
async def cinaprev(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(tvaryny = '')
     tvr = ''

     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + tvr , reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)



    # [InlineKeyboardButton(text='до 12000',callback_data='cinakvartyrado'),InlineKeyboardButton(text='12000 - 16000',callback_data='cinakvartyramishfirst')],
    # [InlineKeyboardButton(text='16000 - 20000',callback_data='cinakvartyramishsecond'),InlineKeyboardButton(text='20000 - 25000',callback_data='cinakvartyramishthird')],
    # [InlineKeyboardButton(text='25000 - 40000',callback_data='cinakvartyramishfour'),InlineKeyboardButton(text='від 40000',callback_data='cinakvartyramishpislia')],
    # [InlineKeyboardButton(text='Назад',callback_data='cinakvartyrastepback')],
@dp.callback_query(F.data=='cinakvartyrado')
async def cinakvartyrado(callback:CallbackQuery, state:FSMContext):
     await state.update_data(cina = 'До 12000')
     data = await state.get_data()
     cn = 'До 12000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=filter_end, parse_mode= ParseMode.HTML)
     text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn
     savefilter(False,str(data["user"].from_user.id),text,data)

@dp.callback_query(F.data=='cinakvartyramishfirst') 
async def cinakvartyramishfirst(callback:CallbackQuery, state:FSMContext):
     await state.update_data(cina = '12000 - 16000')
     data = await state.get_data()
     cn = '12000 - 16000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=filter_end, parse_mode= ParseMode.HTML)
     text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"]  + '\n' +  kimnattext + data["kstkimnat"] +'\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn
     savefilter(False,str(data["user"].from_user.id),text,data)

@dp.callback_query(F.data=='cinakvartyramishsecond')
async def cinakvartyramishsecond(callback:CallbackQuery, state:FSMContext):
     await state.update_data(cina = '16000 - 20000')
     data = await state.get_data()
     cn = '16000 - 20000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=filter_end, parse_mode= ParseMode.HTML)
     text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn
     savefilter(False,str(data["user"].from_user.id),text,data)

@dp.callback_query(F.data=='cinakvartyramishthird')
async def cinakvartyramishthird(callback:CallbackQuery, state:FSMContext):
     await state.update_data(cina = '20000 - 25000')
     data = await state.get_data()
     cn = '20000 - 25000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=filter_end, parse_mode= ParseMode.HTML)
     text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn
     savefilter(False,str(data["user"].from_user.id),text,data)

@dp.callback_query(F.data=='cinakvartyramishfour')
async def cinado(callback:CallbackQuery, state:FSMContext):
     await state.update_data(cina = '25000 - 40000')
     data = await state.get_data()
     cn = '25000 - 40000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=filter_end, parse_mode= ParseMode.HTML)
     text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn
     savefilter(False,str(data["user"].from_user.id),text,data)

@dp.callback_query(F.data=='cinakvartyramishpislia')
async def cinakvartyramishpislia(callback:CallbackQuery, state:FSMContext):
     await state.update_data(cina = 'від 40000')
     data = await state.get_data()
     cn = 'від 40000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=filter_end, parse_mode= ParseMode.HTML)
     text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn
     savefilter(False,str(data["user"].from_user.id),text,data)

@dp.callback_query(F.data=='cinakvartyrastepback')
async def cinakvartyrastepback(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)


#    [InlineKeyboardButton(text='до 12000',callback_data='cinabydunkudo'),InlineKeyboardButton(text='12000 - 20000',callback_data='cinabydunkumishfirst')],
#     [InlineKeyboardButton(text='20000 - 30000',callback_data='cinabydunkumishsecond'),InlineKeyboardButton(text='30000 - 50000',callback_data='cinabydunkumishthird')],
#     [InlineKeyboardButton(text='від 50000',callback_data='cinabydunkumishpislia')],
#     [InlineKeyboardButton(text='Назад',callback_data='cinabydunkustepback')],


@dp.callback_query(F.data=='cinabydunkudo')
async def cinabydunkudo(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = 'До 12000')
     cn = 'До 12000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinabydunkumishfirst')
async def cinabydunkumishfirst(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = '12000 - 20000')
     cn = '12000 - 20000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinabydunkumishsecond')
async def cinabydunkumishsecond(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = '20000 - 30000')
     cn = '20000 - 30000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinabydunkumishthird')
async def cinabydunkumishthird(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = '30000 - 50000')
     cn = '30000 - 50000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='cinabydunkumishpislia')
async def cinabydunkumishpislia(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = 'від 50000')
     cn = 'від 50000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny + data["tvaryny"] + '\n' + cinatext + cn, reply_markup=cina_bydunku_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n' + termin + data["terminorendu"] + '\n' +tvaryny + data["tvaryny"] + '\n' + cinatext + cn, parse_mode= ParseMode.HTML)


@dp.callback_query(F.data=='cinabydunkustepback')
async def cinabydunkustepback(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.update_data(cina = '')
     cn = ''
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' +  kimnattext + data["kstkimnat"] + '\n'+ termin + data["terminorendu"] + '\n' + tvaryny, reply_markup=tvaryny_inline, parse_mode= ParseMode.HTML)
    
    # [InlineKeyboardButton(text='Офіс',callback_data='ofis'),InlineKeyboardButton(text='Торгівля',callback_data='torgivlia')],
    # [InlineKeyboardButton(text='HoReCa',callback_data='horeca'),InlineKeyboardButton(text='Склад',callback_data='sklad')],
    # [InlineKeyboardButton(text='Виробництво',callback_data='vyrobnytstvo'),InlineKeyboardButton(text='Бізнес',callback_data='business')],
    # [InlineKeyboardButton(text='Назад',callback_data='vydvykorystanniastepback')],



@dp.callback_query(F.data=='ofis')
async def ofis(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.vydvykorystannia)
     await state.update_data(vydvykorystannia = 'Офіс')
     vv = 'Офіс'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_vykorystanniatext + vv, reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_vykorystanniatext + vv, parse_mode= ParseMode.HTML)    


@dp.callback_query(F.data=='torgivlia')
async def torgivlia(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.vydvykorystannia)
     await state.update_data(vydvykorystannia = 'Торгівля')
     vv = 'Торгівля'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_vykorystanniatext + vv, reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_vykorystanniatext + vv, parse_mode= ParseMode.HTML)    


@dp.callback_query(F.data=='horeca')
async def horeca(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.vydvykorystannia)
     await state.update_data(vydvykorystannia = 'HoReCa')
     vv = 'HoReCa'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_vykorystanniatext + vv, reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_vykorystanniatext + vv, parse_mode= ParseMode.HTML)    


@dp.callback_query(F.data=='sklad')
async def sklad(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.vydvykorystannia)
     await state.update_data(vydvykorystannia = 'Склад')
     vv = 'Склад'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_vykorystanniatext + vv, reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_vykorystanniatext + vv, parse_mode= ParseMode.HTML)    


@dp.callback_query(F.data=='vyrobnytstvo')
async def vyrobnytstvo(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.vydvykorystannia)
     await state.update_data(vydvykorystannia = 'Виробництво')
     vv = 'Виробництво'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_vykorystanniatext + vv, reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_vykorystanniatext + vv, parse_mode= ParseMode.HTML)    

@dp.callback_query(F.data=='business')
async def business(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.vydvykorystannia)
     await state.update_data(vydvykorystannia = 'Бізнес')
     vv = 'Бізнес'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_vykorystanniatext + vv, reply_markup=vyd_vykorystannia_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>"'\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_vykorystanniatext + vv, parse_mode= ParseMode.HTML)    

@dp.callback_query(F.data=='vydvykorystanniastepback')
async def vydvykorystanniastepback(callback:CallbackQuery, state:FSMContext):

    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.location)
    await state.update_data(vydvykorystannia = '')
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



# [InlineKeyboardButton(text='Гараж',callback_data='mashynomiscegarash'),InlineKeyboardButton(text='Паркомісце',callback_data='mashynomisceparkomisce')],

#     [InlineKeyboardButton(text='Назад',callback_data='vydmashynomiscestepback')],



@dp.callback_query(F.data=='mashynomiscegarash')
async def mashynomiscegarash(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.mashynomisce)
     await state.update_data(mashynomisce = 'Гараж')
     mm = 'Гараж'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_parkomisce + mm + '\n' + cinatext, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='mashynomisceparkomisce')
async def mashynomisceparkomisce(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.mashynomisce)
     await state.update_data(mashynomisce = 'Паркомісце')
     mm = 'Паркомісце'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] +  '\n' + vyd_parkomisce + mm + '\n' + cinatext, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)

@dp.callback_query(F.data=='vydmashynomiscestepback')
async def vydmashynomiscestepback(callback:CallbackQuery, state:FSMContext):
    global rayon_checked
    global rayon_checked_start
    rayon_checked = copy.deepcopy( rayon_checked_start)
    inmarkup = change_rayon('start')
    await state.set_state(Orenda.typeneruxomist)
    await state.update_data(mashynomisce = '')
    await state.set_state(Orenda.location)
    data = await state.get_data()
    loc = ''
    #await callback.message.edit_text( data["orenda"] + '\n' +data["typeneruxomist"], reply_markup=location_inline)
    await callback.message.edit_caption(caption= '\n'+ '\n'+wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] +'\n'+ rayonik + loc , reply_markup=InlineKeyboardMarkup(inline_keyboard=inmarkup), parse_mode= ParseMode.HTML)



    


# cina_mashynomisce_inline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='до 3000',callback_data='cinamashynomiscedo')],
#     [InlineKeyboardButton(text='3000 - 5000',callback_data='cinamashynomiscemish')],
#     [InlineKeyboardButton(text='від 5000',callback_data='cinamashynomiscemishpislia')],
#     [InlineKeyboardButton(text='Назад',callback_data='cinamashynomiscestepback')],
    
#  ])


@dp.callback_query(F.data=='cinamashynomiscedo')
async def cinamashynomiscedo(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.cinamashynomisce)
     await state.update_data(cinamashynomisce = 'до 3000')
     cm = 'до 3000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_parkomisce + data["mashynomisce"] + '\n'  + cinatext + cm, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_parkomisce + data["mashynomisce"] + '\n'  + cinatext + cm , parse_mode= ParseMode.HTML)    


@dp.callback_query(F.data=='cinamashynomiscemish')
async def cinamashynomiscemish(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.cinamashynomisce)
     await state.update_data(cinamashynomisce = '3000 - 5000')
     cm = '3000 - 5000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_parkomisce + data["mashynomisce"] +   '\n'  + cinatext + cm, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"]  + '\n' + vyd_parkomisce + data["mashynomisce"] + '\n' + cinatext + cm, parse_mode= ParseMode.HTML)    

@dp.callback_query(F.data=='cinamashynomiscemishpislia')
async def cinamashynomiscemishpislia(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.cinamashynomisce)
     await state.update_data(cinamashynomisce = 'від 5000')
     cm = 'від 5000'
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_parkomisce + data["mashynomisce"] +   '\n'  + cinatext + cm, reply_markup=cina_mashynomisce_inline, parse_mode= ParseMode.HTML)
     await callback.message.answer(text=  '\n'+ '\n'+ "Ваш фільтр=======>" +  '\n' + '\n' + "Id користувача: " + str(data["user"].from_user.id) + '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"]  + '\n' + vyd_parkomisce + data["mashynomisce"] + '\n' + cinatext + cm, parse_mode= ParseMode.HTML)    


@dp.callback_query(F.data=='cinamashynomiscestepback')
async def cinamashynomiscestepback(callback:CallbackQuery, state:FSMContext):
     data = await state.get_data()
     await state.set_state(Orenda.mashynomisce)
     await state.update_data(cinamashynomisce = '')
     mm = ''
     await callback.message.edit_caption(caption= '\n'+ '\n'+ wesearch +data["orenda"] + '\n' + typener + data["typeneruxomist"] + '\n' + rayonik + '\n' + data["location"] + '\n' + vyd_parkomisce + mm, reply_markup=vyd_mashynomisce_inline, parse_mode= ParseMode.HTML)

# @dp.message(F.photo)
# async def get_photo(message:Message):
#     await message.answer(f'id photo: {message.photo[-1].file_id}')
 


async def main():
    await dp.start_polling(bot) 

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


#kvartirant2024_bot
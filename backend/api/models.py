from django.db import models

# Create your models here.

class Naspunkt(models.Model):
    id = models.AutoField(primary_key=True)
    imja_nas_punkt = models.TextField(db_collation='utf8_general_ci')
    ID_type_nas_punkt = models.IntegerField()
    otg = models.IntegerField()
    ID_rayon = models.TextField(db_collation='utf8_general_ci')
    Link = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "naspunkts"

    def __str__(self):
        return self.name
    

class Rayon(models.Model):
    id = models.AutoField(primary_key=True)
    Nazva_Rayona = models.TextField(db_collation='utf8_general_ci')
    misto = models.IntegerField()

    class Meta:
        db_table = "rayons"

    def __str__(self):
        return self.name
    


class Vulyci(models.Model):
    id = models.AutoField(primary_key=True)
    Name_Vul = models.TextField(db_collation='utf8_general_ci')
    Stara_Nazva1 = models.TextField(db_collation='utf8_general_ci')
    Stara_Nazva2 = models.TextField(db_collation='utf8_general_ci')
    alternative = models.TextField(db_collation='utf8_general_ci')
    IDrayons = models.TextField(db_collation='utf8_general_ci')
    misto = models.IntegerField()
    class Meta:
        db_table = "vulycis"

    def __str__(self):
        return self.name


class Naselenyipunktperedmistia(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(db_collation='utf8_general_ci')

    class Meta:
        db_table = "naselenyipunktperedmistia"

    def __str__(self):
        return self.name
    

class Vulyciperedmist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(db_collation='utf8_general_ci')
    idperedmistia = models.IntegerField()

    class Meta:
        db_table = "vulyciperedmist"

    def __str__(self):
        return self.name


class Testobj(models.Model):
    id = models.AutoField(primary_key=True)
    jsonobj = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "testobj"

    def __str__(self):
        return self.name
    
class Objectneruxomosti(models.Model):
    id = models.AutoField(primary_key=True)
    prodazh = models.BooleanField()
    type_real_estate=models.IntegerField()
    cina=models.FloatField()
    valuta=models.IntegerField()
    komisija=models.FloatField()
    locationid=models.BigIntegerField()
    kstspalenid=models.IntegerField()
    prysnachenniasemliid=models.IntegerField()
    ploshasagalna=models.FloatField()
    ploshakorysna=models.FloatField()
    ploshakuchnia=models.FloatField()
    poverx=models.IntegerField()
    poverxovist=models.IntegerField()
    kstsanvuslivid=models.IntegerField()
    stanid=models.IntegerField()
    opalennia=models.TextField(db_collation='utf8_general_ci')
    materialstinid=models.IntegerField()
    doisd=models.TextField()
    umebliovano=models.BooleanField()
    technika=models.BooleanField()
    umovuprodashuid=models.IntegerField()
    dodatkovoproon=models.TextField(db_collation='utf8_general_ci')
    typebydunokid=models.IntegerField()
    typebydivliaid=models.IntegerField()
    mistoid=models.IntegerField()
    rayonid=models.IntegerField()
    vulicaid=models.IntegerField()
    bydunokaddr=models.IntegerField()
    sectionaddr=models.TextField(db_collation='utf8_general_ci')
    kvartyraaddr=models.IntegerField()
    terminorendu=models.IntegerField()
    avtomiscetype=models.IntegerField()
    ploshadilianku=models.FloatField()
    komunikacii=models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "objectneruxomostis"

    def __str__(self):
        return self.name
    

class Images(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(db_collation='utf8_general_ci')
    dir = models.TextField(db_collation='utf8_general_ci')
    idobject = models.IntegerField()
    class Meta:
        db_table = "images"
    def __str__(self):
        return self.name
    

class Materialstin(models.Model):
    id = models.AutoField(primary_key=True)
    MaterialStin = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "materialstins"
    def __str__(self):
        return self.name
    
class Stan(models.Model):
    id = models.AutoField(primary_key=True)
    stan = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "stan"
    def __str__(self):
        return self.name
    
class Kstspalen(models.Model):
    id = models.AutoField(primary_key=True)
    spalennazva = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "kstspalens"
    def __str__(self):
        return self.name
    
class Budivlia(models.Model):
    id = models.AutoField(primary_key=True)
    budivlia = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "budivlia"
    def __str__(self):
        return self.name
    
class Nevtags(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.TextField(db_collation='utf8_general_ci')
    class Meta:
        db_table = "nevtags"
    def __str__(self):
        return self.name
    
class ObjectneruxomostiNevtag(models.Model):
    id = models.AutoField(primary_key=True)
    objectneruxomosti_id = models.BigIntegerField(20)
    nevtag_id=models.BigIntegerField(20)
    class Meta:
        db_table = "objectneruxomosti_nevtag"
    def __str__(self):
        return self.name
    


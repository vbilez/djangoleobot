from django.db import models

# Create your models here.

class Naspunkt(models.Model):
    id = models.AutoField(primary_key=True)
    imja_nas_punkt = models.TextField(db_collation='ut8_general_ci')
    ID_type_nas_punkt = models.IntegerField()
    ID_rayon = models.TextField(db_collation='ut8_general_ci')
    Link = models.TextField(db_collation='ut8_general_ci')
    class Meta:
        db_table = "naspunkts"

    def __str__(self):
        return self.name
    

class Rayon(models.Model):
    id = models.AutoField(primary_key=True)
    Nazva_Rayona = models.TextField(db_collation='ut8_general_ci')
    misto = models.IntegerField()

    class Meta:
        db_table = "rayons"

    def __str__(self):
        return self.name
    


class Vulyci(models.Model):
    id = models.AutoField(primary_key=True)
    Name_Vul = models.TextField(db_collation='ut8_general_ci')
    Stara_Nazva1 = models.TextField(db_collation='ut8_general_ci')
    Stara_Nazva2 = models.TextField(db_collation='ut8_general_ci')
    alternative = models.TextField(db_collation='ut8_general_ci')
    IDrayons = models.TextField(db_collation='ut8_general_ci')
    class Meta:
        db_table = "vulycis"

    def __str__(self):
        return self.name

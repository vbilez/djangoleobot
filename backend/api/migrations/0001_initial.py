# Generated by Django 5.0.6 on 2024-06-24 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
 
 
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Naselenyipunktperedmistia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(db_collation='utf8_general_ci')),
            ],
            options={
                'db_table': 'naselenyipunktperedmistia',
            },
        ),
   
        migrations.CreateModel(
            name='Naspunkt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imja_nas_punkt', models.TextField(db_collation='utf8_general_ci')),
                ('ID_type_nas_punkt', models.IntegerField()),
                ('ID_rayon', models.TextField(db_collation='utf8_general_ci')),
                ('Link', models.TextField(db_collation='utf8_general_ci')),
            ],
            options={
                'db_table': 'naspunkts',
            },
        ),
        migrations.CreateModel(
            name='Rayon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Nazva_Rayona', models.TextField(db_collation='utf8_general_ci')),
                ('misto', models.IntegerField()),
            ],
            options={
                'db_table': 'rayons',
            },
        ),
        migrations.CreateModel(
            name='Vulyci',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name_Vul', models.TextField(db_collation='utf8_general_ci')),
                ('Stara_Nazva1', models.TextField(db_collation='utf8_general_ci')),
                ('Stara_Nazva2', models.TextField(db_collation='utf8_general_ci')),
                ('alternative', models.TextField(db_collation='utf8_general_ci')),
                ('IDrayons', models.TextField(db_collation='utf8_general_ci')),
            ],
            options={
                'db_table': 'vulycis',
            },
        ),
        
    ]
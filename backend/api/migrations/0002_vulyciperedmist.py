# Generated by Django 5.0.6 on 2024-06-25 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vulyciperedmist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(db_collation='utf8_general_ci')),
                ('idperedmistia', models.IntegerField()),
            ],
            options={
                'db_table': 'vulyciperedmist',
            },
        ),
    ]
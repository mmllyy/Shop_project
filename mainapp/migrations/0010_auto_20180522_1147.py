# Generated by Django 2.0.5 on 2018-05-22 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20180522_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('typeid', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('typename', models.CharField(max_length=50)),
                ('childtypenames', models.CharField(max_length=200)),
                ('typesort', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_foodtypes',
            },
        ),
        migrations.DeleteModel(
            name='MainShow',
        ),
    ]

# Generated by Django 2.0.5 on 2018-05-22 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20180522_1022'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='brandproduct',
            table='axf_brand_product',
        ),
        migrations.AlterModelTable(
            name='mainshowparent',
            table='axf_brand',
        ),
    ]

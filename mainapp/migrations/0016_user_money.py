# Generated by Django 2.0.5 on 2018-05-26 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20180525_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]

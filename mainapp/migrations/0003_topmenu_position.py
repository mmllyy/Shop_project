# Generated by Django 2.0.5 on 2018-05-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_topmenu'),
    ]

    operations = [
        migrations.AddField(
            model_name='topmenu',
            name='position',
            field=models.IntegerField(default=1),
        ),
    ]
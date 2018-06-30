# Generated by Django 2.0.5 on 2018-05-21 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopWheel',
            fields=[
                ('trackid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('img', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'axf_wheel',
            },
        ),
    ]

# Generated by Django 2.0.5 on 2018-05-25 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_cart_deliveryaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderNum', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='订单号')),
                ('orderPrice', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payState', models.IntegerField(choices=[(0, '待支付'), (1, '已支付'), (2, '正在支付中'), (3, '已退款')], default=0)),
                ('payType', models.IntegerField(choices=[(0, '余款'), (1, '支付宝'), (2, '微信')], default=0)),
                ('orderState', models.IntegerField(choices=[(0, '待派送'), (1, '已派送'), (2, '已到达'), (3, '已签收'), (4, '拒收'), (5, '未到达')], default=0)),
                ('orderTime', models.DateTimeField(auto_now_add=True)),
                ('orderLastTime', models.DateTimeField(auto_now=True)),
                ('orderAdress', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.DeliveryAddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.User')),
            ],
            options={
                'db_table': 'axf_order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='小计')),
                ('goods', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Goods')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Order')),
            ],
            options={
                'db_table': 'axf_order_goods',
            },
        ),
    ]

import hashlib
import uuid

import os

from io import BytesIO
from random import random

import time
from AXF_project import settings
from PIL import Image, ImageDraw, ImageFont
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from mainapp.models import *


def home(request):
    wheelsList = TopWheel.objects.all()
    navList = TopMenu.objects.all()
    mustbuyList = Mustbuy.objects.all()

    shopList = Shop.objects.all().order_by('position')
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    brandList = MainShowParent.objects.all()


    return render(request, 'home.html', {"title":"主页",
                                             "topWheels":wheelsList,
                                             "topMenus":navList,
                                             "mustbuylist":mustbuyList,
                                             "shop1":shop1,
                                             "shop2":shop2,
                                             "shop3":shop3,
                                             "shop4":shop4,
                                             "brandList":brandList})



def market(req, categoryid=0, childid=0, sortid=0):
    goodsList = None

    sortColumn = 'productid'  # 设置排序的列
    if sortid == 1:
        sortColumn = '-price'  # 价格最高
    elif sortid == 2:
        sortColumn = 'price'  # 价格最低
    elif sortid == 3:
        sortColumn = '-productnum'  # 销量最高

    # 获取所有子类型
    childTypes = []

    if categoryid:
        # 获取所有的子类型
        # 全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540
        cTypes = FoodType.objects.filter(typeid=categoryid).last().childtypenames
        cTypes = cTypes.split('#')
        for ctype in cTypes:
            ctype = ctype.split(":")
            childTypes.append({"name": ctype[0], "id": ctype[1]})

        if childid:
            goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid).order_by(sortColumn)
        else:
            goodsList = Goods.objects.filter(categoryid=categoryid).order_by(sortColumn)
    else:
        goodsList = Goods.objects.all().order_by(sortColumn)[0:20]

    return render(req, 'market.html',
                  {'title': '闪购',
                   "foodTypes": FoodType.objects.all().order_by('typesort'),
                   'goodsList': goodsList,
                   'categoryid': str(categoryid),
                   'childTypes': childTypes,
                   'childid': str(childid),
                   'sortid': sortid})


def cart(request):
    return render(request,'cart.html',{'title':'购物车'})


def mine(req):
    if not req.COOKIES.get('token'):
        return HttpResponseRedirect('/app/login')

    return render(req, 'mine.html',
                  {'navs': getMyOrderNav(),
                   'menus': getMyOrderMenu(),
                   'loginUser':User.objects.filter(token=req.COOKIES.get('token')).first()})


def getMyOrderNav():
    navs = []
    navs.append({'name': '待付款', 'icon':'glyphicon glyphicon-usd', 'url':'#'})
    navs.append({'name': '待收货', 'icon': 'glyphicon glyphicon-envelope', 'url':'#'})
    navs.append({'name': '待评价', 'icon': 'glyphicon glyphicon-pencil','url':'#'})
    navs.append({'name': '退款/售后', 'icon': 'glyphicon glyphicon-retweet', 'url':'#'})

    return navs

def getMyOrderMenu():
    menus = []
    menus.append({'name': '积分商城', 'icon':'glyphicon glyphicon-bullhorn','url':'#'})
    menus.append({'name': '优惠券', 'icon': 'glyphicon glyphicon-credit-card','url':'#'})
    menus.append({'name': '收货地址', 'icon': 'glyphicon glyphicon-import','url':'#'})
    menus.append({'name': '客服/反馈', 'icon': 'glyphicon glyphicon-phone-alt','url':'#'})
    menus.append({'name': '关于我们', 'icon': 'glyphicon glyphicon-asterisk', 'url':'#'})

    return menus


def regist(req):
    if req.method == 'GET':
        return render(req, 'regist.html')
    user = User()
    user.userName = req.POST.get('username')
    user.userPasswd = crypt(req.POST.get('passwd'))
    user.phone = req.POST.get('phone')
    user.nickName = req.POST.get('nickname')

    user.token = newToken(user.userName)
    user.save()
    resp = HttpResponseRedirect('/app/mine')
    resp.set_cookie('token',user.token)

    return resp


def newToken(userName):
    # uuid + 用户名
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4())+userName).encode())
    return md5.hexdigest()

def crypt(pwd, cryptName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()


@csrf_exempt  # 不做csrf_token验证
def upload(req):
    msg = {}
    cookie_token = req.COOKIES.get('token')
    if not cookie_token:
        msg['state'] = 'fail'
        msg['msg'] = '请先登录'
        msg['code'] = '201'
    else:
        qs = User.objects.filter(token=cookie_token)
        if not qs.exists():
            msg['state'] = 'fail'
            msg['msg'] = '登录失效，请重新登录'
            msg['code'] = '202'
        else:
            # 开始上传
            uploadFile = req.FILES.get('img')

            saveFileName = newFileName(uploadFile.content_type)
            saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)

            # 将上传文件的数据分段写入到目标文件（存放到当前服务端）中
            with open(saveFilePath, 'wb') as f:
                for part in uploadFile.chunks():
                    f.write(part)
                    f.flush()

            # 将上传文件的路径更新到用户
            qs.update(imgPath='upload/'+saveFileName)

            msg['state'] = 'ok'
            msg['msg'] = '上传成功'
            msg['code'] = '200'
            msg['path'] = 'upload/'+saveFileName

    return JsonResponse(msg)


def newFileName(contentType):
    fileName = crypt(str(uuid.uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName  = '.png'

    return fileName+extName


def logout(req):
    resp = HttpResponseRedirect('/app/login')
    if req.COOKIES.get('token'):
        # 解除和用户绑定的token
        User.objects.filter(token=req.COOKIES.get('token')).update(token='')

        # 从Cookie中删除
        resp.delete_cookie('token')

    return resp


def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')

    username = req.POST.get('username')
    passwd = req.POST.get('passwd')

    qs = User.objects.filter(userName=username,
                             userPasswd=crypt(passwd))
    if qs.exists():
        user = qs.first()
        # 向session中存放user_id, 用于购物车
        req.session['user_id'] = user.id
        # 更新用户的token
        user.token = newToken(user.userName)
        user.save()
        # 用户登录成功
        resp = HttpResponseRedirect('/app/mine')
        # 向客户端添加cookie
        resp.set_cookie('token', user.token)
        return resp
    else:
        return render(req, 'login.html',
                      {'error_msg':'用户登录失败，请重试'})


def verifycode(req):
    # 1. 创建画布Image对象
    img = Image.new(mode='RGB', size=(120, 30), color=(220, 220, 180))

    # 2. 创建画笔 ImageDraw对象
    draw = ImageDraw.Draw(img, 'RGB')

    # 3. 画文本，画点，画线
    # 随机产生0-9, A-Z, a-z范围的字符
    chars = ''
    while len(chars) < 4:
        flag = random.randrange(3)
        char = chr(random.randint(48, 57)) if not flag else \
                  chr(random.randint(65, 90)) if flag == 1 else \
                  chr(random.randint(97, 122))
        # 排除重复的
        if len(chars) == 0 or chars.find(char) == -1:
            chars += char

    # 将生成的验证码的字符串存入到session中
    req.session['verifycode'] = chars

    font = ImageFont.truetype(font='static/fonts/hktt.ttf', size=25)
    for char in chars:
        xy = (15+chars.find(char)*20, random.randrange(2, 8))
        draw.text(xy=xy,
                  text=char,
                  fill=(255, 0, 0),
                  font=font)
    for i in range(200):
        xy = (random.randrange(120), random.randrange(30))
        color = (random.randrange(255),
                 random.randrange(255),
                 random.randrange(255))
        draw.point(xy=xy, fill=color)

    # 4. 将画布对象转成字节数据
    buffer = BytesIO()  # 缓存
    img.save(buffer, 'png')  # 指定的图片格式为png

    # 5. 清场(删除对象的引用)
    del draw
    del img
    return HttpResponse(buffer.getvalue(),  # 从BytesIO对象中获取字节数据
                        content_type='image/png')


def cart(req):
    # 确认用户是否登录
    user_id = req.session.get('user_id')
    if not user_id:
        return render(req, 'login.html',
                      {'title':'用户登录'})

    # 查询当前用户的默认收货信息
    deliveryAddress = DeliveryAddress.objects.filter(user_id=user_id).first()

    # 查看当前用户下的购物车中的商品信息
    carts = Cart.objects.filter(user_id=user_id)
    totalPrice = 0  # 计算总价格
    for cart in carts:
        if cart.isSelected:
            totalPrice += cart.goods.price*cart.cnt

    return render(req,
                  'cart.html',
                  {'title': '购物车',
                   'myAddress': deliveryAddress,
                   'carts': carts,
                   'totalPrice': totalPrice} )


def selectCart(req, cart_id):
    # 0 全选， 99999 取消全选
    if cart_id == 0 or cart_id == 99999:
        # 全部更新
        carts = Cart.objects.filter(user_id=req.session.get('user_id'))
        carts.update(isSelected=True if cart_id == 0 else False)
        totalPrice = 0  # 统计全选时的总价格
        if cart_id == 0:
            for cart in carts:
                totalPrice += cart.cnt * cart.goods.price
        return JsonResponse({'price': totalPrice,
                             'status': 200})

    data = {'status':200,'price': 1000.5}
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.isSelected = not cart.isSelected
        cart.save()
        data['price'] = cart.cnt*cart.goods.price
        data['selected'] = cart.isSelected  # 当前选择状态
    except:
        data['status'] = 300
        data['price'] = 0

    return JsonResponse(data)


def subShopping(req,cart_id):
    data = {'status': 200}
    qs = Cart.objects.filter(id=cart_id)
    if qs.exists():
        price = qs.first().goods.price
        if qs.first().cnt:
            qs.update(cnt=F('cnt')-1)
        qs.first().save()
        data['price']=price
        data['selected'] = qs.first().isSelected
        data['cnt']= qs.first().cnt
    return JsonResponse(data)


def addShopping(req,cart_id):
    data = {'status': 200}
    qs = Cart.objects.filter(id=cart_id)
    if qs.exists():
        price = qs.first().goods.price
        qs.update(cnt=F('cnt') + 1)
        qs.first().save()
        data['price'] = price
        data['selected'] = qs.first().isSelected
    return JsonResponse(data)


def createOrderNum():  # 生成订单号
    orderNum = '0029'+str(time.time()).replace('.', '')[-10:]
    return orderNum


def order(req, num):
    user_id = req.session.get('user_id')
    if not user_id:  # 如果用户没有登录，则进入登录页面
        return render(req, 'login.html')

    order = None
    if num == '0':
        # 下订单
        order = Order()
        order.user_id = user_id

        # 获取用户的第一个收货地址 作为订单的收货地址
        order.orderAdress_id = User.objects.get(pk=user_id).deliveryaddress_set.first().pk

        # 设置订单号
        order.orderNum = createOrderNum()

        # 设置订单金额
        # 1. 查询当前用户下的购物车中所有选择的商品
        carts = Cart.objects.filter(isSelected=True, user_id=user_id)

        if carts.count() == 0:
            return HttpResponseRedirect('/app/cart')

        order.save()  # 保存订单

        # 2. 统计订单总金额 和 将商品插入到订单明细中
        order.orderPrice = 0
        for cart in carts:
            order.orderPrice += cart.cnt * cart.goods.price

            # 创建订单明细对象
            ordergoods = OrderGoods()
            ordergoods.order_id = order.orderNum
            ordergoods.goods_id = cart.goods.pk
            ordergoods.cnt = cart.cnt
            ordergoods.price = cart.cnt * cart.goods.price

            ordergoods.save()

        # 保存订单
        order.save()  # 更新订单总额

        carts.delete()  # 删除购物车中已购买的商品
    else:  # 查询订单
        order = Order.objects.get(pk=num)
    return render(req, 'order.html',
                  {'title': '我的订单',
                   'order': order})


def pay(req, num, payType=0):
    try:
        order = Order.objects.get(pk=num)
        order.payType = payType

        # 必须要先登录
        user = User.objects.get(pk=req.session.get('user_id'))

        if user.money < order.orderPrice:
            return JsonResponse({'status': 'fail',
                                 'msg': '余款不足!'})
        else:
            user.money -= order.orderPrice
            user.save()
            order.payState=1 # 已支付
            order.save()

            # 减去库存量
            # 优化业务 ：在添加到购物车时，判断商品的库存量，如果不足，则提示
            for item in order.ordergoods_set.all():
                goods = item.goods
                goods.productnum += item.cnt  # 销售量
                goods.storenums -= item.cnt  # 库存量
                goods.save()

    except:
        return JsonResponse({'status': 'fail',
                             'msg': '支付失败!'})

    return JsonResponse({'status': 'ok',
                         'msg':'支付成功!'})
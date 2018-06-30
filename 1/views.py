from django.shortcuts import render

# Create your views here.
from mainapp.models import TopWheel, TopMenu, TopShop, MustBuy, MainShow, MainShowBrand, FoodType, Goods


def home(req):
    shopList = TopShop.objects.all().order_by('position')
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    return render(req, "home.html",
                  {"title": "主页",
                   "topWheels": TopWheel.objects.all(),
                   "topMenus": TopMenu.objects.all().order_by('position'),
                   "mustbuys": MustBuy.objects.all(),
                   "shop1": shop1,
                   "shop2": shop2,
                   "shop3": shop3,
                   "shop4": shop4,
                   "mainShows": MainShowBrand.objects.all()})

def market(req, categoryid=0, childid=0,sortid=0):
    goodsList = None

    sortColumn = 'productid'  # 设置排序的列
    if sortid == 1:
        sortColumn = '-price'  # 价格最高
    elif sortid == 2:
        sortColumn = 'price'  # 价格最低
    elif sortid == 3:
        sortColumn = '-productnum'  #销量最高

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
                   'sortid': sortid })

def mine(req):
    return render(req, 'mine.html',
                  {'navs': getMyOrderNav(),
                   'menus': getMyOrderMenu()})


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
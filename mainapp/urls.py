import mainapp
from django.contrib import admin
from django.urls import path, include
from mainapp import views

urlpatterns = [
    path('', views.home),
    path('market/<int:categoryid>/<int:childid>/<int:sortid>', views.market),
    path('cart', views.cart),
    path('mine', views.mine),
    path('regist', views.regist),
    path('upload', views.upload),
    path('logout', views.logout),
    path('login', views.login),
    path('cart', views.cart),
    path('select/<int:cart_id>', views.selectCart),
    path('subShopping/<int:cart_id>', views.subShopping),
    path('addShopping/<int:cart_id>', views.addShopping),
    path('order/<str:num>', views.order),
    path('pay/<str:num>/<int:payType>',views.pay)
]

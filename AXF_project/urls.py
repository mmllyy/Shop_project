import mainapp
from django.contrib import admin
from django.urls import path, include
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('app/', include('mainapp.urls')),
]

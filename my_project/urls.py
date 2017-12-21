"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url, include
from app1 import views
import os

urlpatterns =[
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^$',views.home, name='home'),   #开始可以是home页，也可以改为login页，login页有register页的链接
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^goodDisplay/$', views.goodDisplay, name='index1'), #和顾客登陆后页面是同一个，只不过返回的参数变成了类别商品
    url(r'^getcomplaintEntry/$', views.complaintEntry, name='complaintEntry'),
]




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
    url(r'^goodDisplay/$', views.goodDisplay, name='goodDisplay'), #和顾客登陆后页面是同一个，只不过返回的参数变成了类别商品
    url(r'^search/$', views.search, name='search'),
    url(r'^getRecommendations/$', views.getRecommendations, name='getRecommendations'),
    url(r'^customerInfoDisplay/$',views.customerInfoDisplay,name='customerInfoDisplay'),
    url(r'^complaintDisplay/$', views.complaintDisplay, name='complaintDisplay'),
    url(r'^getComplaintEntry/$', views.getComplaintEntry, name='complaintEntry'),
    url(r'^addComplaint/$',views.addComplaint, name='addComplaint'),
    url(r'^allComplaintEntry/$',views.allComplaintEntry, name='allComplaintEntry'),
    url(r'^submitComplaint/$',views.submitComplaint, name='submitComplaint'),
    url(r'^getComplaintWork/$', views.getComplaintWork, name='getComplaintWork'),
    url(r'^static/managerComplaintEntry/$', views.managerComplaintEntry, name='managerComplaintEntry'),
    url(r'^replyToComplaint/$', views.replyToComplaint, name='replyToComplaint'),
    url(r'^addGood/$', views.addGood, name='addGood'),
    url(r'^orderEntry/$', views.orderEntry, name='orderEntry'),
    url(r'^getShoppingList/$', views.getShoppingList, name='getShoppingList'),
    url(r'^submitShoppingList/$', views.submitShoppingList, name='submitShoppingList'),
    url(r'^getOrderWork/$', views.getOrderWork, name='getOrderWork'),
    url(r'^changeOrderStatus/$', views.changeOrderStatus, name='changeOrderStatus'),
    url(r'^getPrivilege/$', views.getPrivilege),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^editCustomerInfo/$', views.editCustomerInfo, name='editCustomerInfo'),
    url(r'^getCustomerInfo/$', views.getCustomerInfo, name='getCustomerInfo'),
]

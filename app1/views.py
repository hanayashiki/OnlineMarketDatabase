# coding:utf-8
from django.shortcuts import render
import json
from .forms import customersForm,managersForm
from .models import customers,managers   #这个点必须要加


from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

#注册
def regist(request):
    if request.method =='GET':
        cf=customersForm(request.GET)
        if cf.is_valid():
            name=cf.cleaned_data['name']
            email = cf.cleaned_data['email']
            address = cf.cleaned_data['address']
            telephone = cf.cleaned_data['telephone']
            password = cf.cleaned_data['password']
            confirm_password = cf.cleaned_data['confirm_password']
            customers.objects.create(name=name, email=email, telephone=telephone, address=address, password=password)
            success={"info":"regist success"}
            return HttpResponse(json.dumps(success), content_type="application/json")
    else:
        cf=customersForm()
    return render(request,'register.html', locals())

#登录
def login(request):
    if(request.method=='GET'):
        cf=customersForm(request.GET)
        mf=managersForm(request.GET)
        if cf.is_valid():
            name=cf.cleaned_data['name']
            password=cf.cleaned_data['password']
            customer=customers.objects.filter(name_exact=name, password_exact=password)
            if customer:
                response=HttpResponseRedirect('/index1/')   #顾客登陆成功就跳转到index
                response.set_cookie('name', name, 3600)
                return response
            else:
                return HttpResponseRedirect('/login/')
        else:
            if mf.is_valid():
                name = cf.cleaned_data['name']
                password = cf.cleaned_data['password']
                manager = managers.objects.filter(name_exact=name, password_exact=password)
                if manager:
                    response = HttpResponseRedirect('/index2/')  #管理员登陆成功就跳转到index2
                    response.set_cookie('name', name, 3600)
                    return response
                else:
                    return HttpResponseRedirect('/login/')
    else:
        cf=customersForm()
    return render(request,'login.html', locals())

#登陆成功
def index1(request):
    name=request.COOKIES.get('name', '')
    return render(request, 'index1.html', locals())

def index2(request):
    name=request.COOKIES.get('name', '')
    return render(request, 'index2.html', locals())

#登录失败
def logout(request):
    fail = {"info": "regist success"}
    response=HttpResponse(json.dumps(fail), content_type="application/json")
    response.delete_cookie('name')
    return response


def home(request):
    return render(request, 'home.html')

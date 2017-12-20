# coding:utf-8
from django.shortcuts import render
import json
from .forms import customersregistForm, customersForm
from .models import customers,managers,complaints, goods   #这个点必须要加


from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
#主页面（也可以上来就是登录页面，有个按钮跳到注册页面）
def home(request):
    return render(request, 'home.html')
#注册
def regist(request):
    if request.method =='POST':
        cf=customersregistForm(request.POST)
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
#登陆成功后的index1和index2页面的不同就在于右上角个人信息与投诉信息不同（分管理员的和顾客的）
def login(request):
    if(request.method=='POST'):
        cf=customersForm(request.POST)
        mf=cf
        if ( cf.is_valid() and  mf.is_valid() ):  #这两个肯定可以同时接收到数据
            name=cf.cleaned_data['name']
            password=cf.cleaned_data['password']
            customer=customers.objects.filter(name_exact=name, password_exact=password) #返回符合姓名和密码的顾客
            manager=managers.objects.filter(name_exact=name, password_exact=password)#返回符合姓名和密码的管理员
            if customer:#顾客的匹配上了
                response=HttpResponseRedirect('/index1/')  #成功登陆转到index1
                response.set_cookie('name', name, 3600)  #cookies操作
                return response
            else:  #顾客的没匹配上（要求manager和顾客不能重名）
                name = cf.cleaned_data['name']
                password = cf.cleaned_data['password']
                manager = managers.objects.filter(name_exact=name, password_exact=password) #匹配管理员的
                if manager: #管理员的匹配上了
                    response = HttpResponseRedirect('/index2/')  # 成功登陆转到index2
                    response.set_cookie('name', name, 3600)
                    return response
                else:
                    return HttpResponseRedirect('/login/')#顾客和管理员都登录不成功就继续返回登录页面
    else:
        cf=customersForm()
        mf=cf
    return render(request,'login.html', locals())

#登陆成功
def index1(request):
    name=request.COOKIES.get('name', '')
    customer = customers.objects.filter(name_exact=name)  # 返回符合姓名和密码的顾客
    customerInfoReturn = {
        "customer_id": customer.customer_id,
        "name": name
    }
    customerInfoReturn = json.dumps(customerInfoReturn)  # 需要的json格式的数据（顾客信息）

    complaint = complaints.objects.filter(customer_id_exact=customer.customer_id).order_by("submit_date").reverse().values(
        "complaint_id", "text", "status", "submit_date") #按日期检索该顾客的投诉信息
    complaintReturn = json.dumps(complaint)
    # 需要的json格式的投诉信息,comlaintReturn是这个顾客的所有投诉信息

    allgoods = goods.object.values("good_id", "name", "price", "image_path", "remain")
    goodsReturn=json.dumps(allgoods)#未选择类别时自动显示所有商品信息

    ##########################################################################以上是顾客登陆后看到的页面，之后是跳转渲染






    return render(request, 'index1.html',
                      {'customerInfoReturn': customerInfoReturn,
                       'complaintReturn': complaintReturn,
                       'goodsReturn': goodsReturn})  # 顾客登陆成功携带json数据返回到index1页面

def index2(request):
    name=request.COOKIES.get('name', '')
    manager = managers.objects.filter(name_exact=name)  # 返回符合姓名和密码的管理员
    managerInfoReturn = {
        "manager_id": manager.manager_id,
        "name": name
    }
    managerInfoReturn = json.dumps(managerInfoReturn)  # 需要的json格式的数据（管理员信息）
    complaint = complaints.objects.filter(manager_id_exact=manager.manager_id).order_by("submit_date").reverse().values(
        "complaint_id", "text", "status", "submit_date")#按日期检索该顾客的投诉信息
    complaintReturn = json.dumps(complaint)
    # 需要的json格式的投诉信息,comlaintReturn是这个管理员要处理的所有投诉信息

    allgoods = goods.object.values("good_id", "name", "price", "image_path", "remain")
    goodsReturn=json.dumps(allgoods)#未选择类别时自动显示所有商品信息

    return render(request, 'index2.html',
                      {'managerInfoReturn': managerInfoReturn,
                       'complaintReturn': complaintReturn,
                       'goodsReturn': goodsReturn})  # 携带json数据返回到index2页面


#登录失败
def logout(request):
    fail = {"info": "regist success"}
    response=HttpResponse(json.dumps(fail), content_type="application/json")
    response.delete_cookie('name')
    return response





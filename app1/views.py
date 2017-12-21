# coding:utf-8
from django.shortcuts import render
import json
from .forms import CustomersregistForm, CustomersForm
from .models import Customers,Managers,Complaints, Goods   #这个点必须要加
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#主页面（也可以上来就是登录页面，有个按钮跳到注册页面）
def home(request):
    return render(request, 'home.html')
#注册
def register(request):
    if request.method =='POST':   #POST!!
        cf=CustomersregistForm(request.POST)
        if cf.is_valid():
            name=cf.cleaned_data['name']
            email = cf.cleaned_data['email']
            address = cf.cleaned_data['address']
            telephone = cf.cleaned_data['telephone']
            password = cf.cleaned_data['password']
            confirm_password = cf.cleaned_data['confirm_password']
            if not (password == confirm_password):
                fail = {"info": "confirm_password and password are different"}
                return HttpResponse(json.dumps(fail), content_type="application/json")
            Customers.objects.create(name=name, email=email, telephone=telephone, address=address, password=password)
            success={'info': "regist success"}
            return HttpResponse(json.dumps(success), content_type="application/json") #注册成功就跳到登录页面
    else:
        cf=CustomersForm()
    return render(request, 'register.html', locals())

#登录
#登陆成功后的index1和index2页面的不同就在于右上角个人信息与投诉信息不同（分管理员的和顾客的）
@csrf_exempt
def login(request):
    if(request.method=='POST'):     #POST！！
        cf=CustomersForm(request.POST)
        mf=cf
        if ( cf.is_valid() and  mf.is_valid() ):  #这两个肯定可以同时接收到数据
            name=cf.cleaned_data['name']
            password=cf.cleaned_data['password']
            customer=Customers.objects.filter(name=name, password=password) #返回符合姓名和密码的顾客
            manager=Managers.objects.filter(name=name, password=password)#返回符合姓名和密码的管理员
            if customer:#顾客的匹配上了
                success = {'info': "login success"}
                response= HttpResponse(json.dumps(success), content_type="application/json")
                response.set_cookie('name', name, 3600)  #cookies操作
                return response
            else:  #顾客的没匹配上（要求manager和顾客不能重名）
                if manager: #管理员的匹配上了
                    success = {'info': "login success"}
                    response = HttpResponse(json.dumps(success), content_type="application/json")
                    response.set_cookie('name', name, 3600)
                    return response
                else:
                    fail= {'info': "login fail"}
                    response=HttpResponse(json.dumps(fail), content_type="application/json")
                    response.delete_cookie('name')
                    return response #顾客和管理员都登录不成功就返回登录失败页面
    else:
        cf=CustomersForm()
        mf=cf
        return render(request, 'login.html', locals())


def customerInfoDisplay(request):
    name = request.COOKIES.get('name', '')
    customer = Customers.objects.filter(name=name)  # 返回符合姓名的顾客
    manager = Managers.objects.filter(name=name)  # 返回符合姓名和密码的管理员
    if customer:
        customerInfoReturn = {
            "customer_id": customer.customer_id,
            "name": name
        }
    if manager:
        customerInfoReturn = {
            "manager_id": manager.manager_id,
            "name": name
        }
    return HttpResponse(json.dumps(list(customerInfoReturn)), content_type="application/json")


def complaintDisplay(request):
    name=request.COOKIES.get('name', '')
    customer = Customers.objects.filter(name=name)
    manager = Managers.objects.filter(name=name)  # 返回符合姓名和密码的管理员
    if customer:
        complaint = Complaints.objects.filter(customer_id=customer.customer_id).order_by(
            "submit_date").reverse().values(
            "complaint_id", "text", "status", "submit_date")  # 按日期检索该顾客的投诉信息
        complaintReturn = json.dumps(list(complaint))
        # 需要的json格式的投诉信息,complaintReturn是这个顾客的所有投诉信息
    if manager:
        complaint = Complaints.objects.filter(manager_id=manager.manager_id).order_by("submit_date").reverse().values(
            "complaint_id", "text", "status", "submit_date")#按日期检索该顾客的投诉信息
        complaintReturn = json.dumps(list(complaint))
    # 需要的json格式的投诉信息,comlaintReturn是这个管理员要处理的所有投诉信息
    return HttpResponse(complaintReturn, content_type="application/json")


def goodDisplay(request):
    somegoods = Goods.objects.values("good_id", "name", "price", "image_path", "remain")

    goodReturn = json.dumps(list(somegoods))  # 未选择类别时自动显示所有商品信息
#    print(goodReturn)
    if(request.method == 'GET'):  #按类别搜索后的结果
        category = request.GET.get('category', "All") #未选择时记为All
        if(category == "All"):
            somegoods = Goods.objects.values("good_id", "name", "price", "image_path", "remain")
           # 未选择类别时自动显示所有商品信息
        else:
            #somegoods=Goods.objects.filter(type=category).values("good_id", "name", "price", "image_path", "remain")
            somegoods = Goods.objects.values("good_id", "name", "price", "image_path", "remain")

        goodReturn = json.dumps(list(somegoods))  # 未选择类别时自动显示所有商品信息

    return HttpResponse(goodReturn, content_type="application/json")


#顾客的，点击投诉信息，查看这一条的信息（以及源头投诉的）
def complaintEntry(request):
    if(request.method == 'GET'):
        complaint_list=[]
        complaint_id = request.GET.get('complain_id')
        complaint = Complaints.objects.filter(complaint_id=complaint_id)   #这一条投诉信息
        source_cmplt_id=complaint.source_cmplt_id
        if source_cmplt_id:  #是系列投诉
            complaint = Complaints.objects.filter(complaint_id=source_cmplt_id)
            complaint_list.append({'text': complaint.text,
                                   'reply': complaint.reply,
                                   'submit_date': complaint.submit_date,
                                   'proceed_date': complaint.proceed_date,
                                   'status': complaint.status})
            while complaint.follow_cmplt_id: #系列还没断
                complaint = Complaints.objects.filter(complaint_id=complaint.follow_cmplt_id)
                complaint_list.append({'text': complaint.text,
                                       'reply': complaint.reply,
                                       'submit_date': complaint.submit_date,
                                       'proceed_date': complaint.proceed_date,
                                       'status': complaint.status})
        else:
            complaint_list.append({'text': complaint.text,
                                   'reply': complaint.reply,
                                   'submit_date': complaint.submit_date,
                                   'proceed_date': complaint.proceed_date,
                                   'status': complaint.status})          #把相关投诉的信息存到了complaint_list里
        complaint_list = json.dumps(list(complaint_list))
        return render(request, 'complaint.html', {'complaint_list': complaint_list})


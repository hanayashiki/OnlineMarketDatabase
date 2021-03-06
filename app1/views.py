#coding=utf-8
from django.shortcuts import render
from django.utils import timezone
import json, random,datetime,time
from app1.forms import CustomersregistForm, CustomersForm
from app1.models import Customers,Managers,Complaints, Goods, Orders
from misc.log import LOG_DEBUG,LOG_ERROR,LOG_INFO
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.utils.encoding import smart_str


# Create your views here.
#主页面（也可以上来就是登录页面，有个按钮跳到注册页面）

def home(request):
    return HttpResponseRedirect('/static/home.html')


    
    
#注册(只有顾客可以注册，管理员不注册)
@csrf_exempt
def register(request):
    LOG_DEBUG("用户注册")
    if request.method =='POST':   #POST!!
        cf=CustomersregistForm(request.POST)
        print(cf)
        if cf.is_valid():
            name = cf.cleaned_data['name']
            email = cf.cleaned_data['email']
            address = cf.cleaned_data['address']
            telephone = cf.cleaned_data['telephone']
            password = cf.cleaned_data['password']
            #检查是不是有重名现象
            nameerror = Customers.objects.raw('select id from Customers where name=%s',[name])
            nameerror = [nameId.id for nameId in nameerror]
            emailerror = Customers.objects.raw('select id from Customers where email=%s',[email])

            emailerror = [emailId.id for emailId in emailerror]
            telephoneerror = Customers.objects.raw('select id from Customers where telephone=%s',[telephone])
            telephoneerror = [telephoneerrorId.id for telephoneerrorId in telephoneerror]

            if(nameerror or emailerror or telephoneerror):
                fail = {'info': "failure"}
                return HttpResponse(json.dumps(fail), content_type="application/json")
            # 不重复就填到表里
            else:
                LOG_DEBUG("用户注册：在数据库中新建用户")
                insert_sql = 'insert into Customers ' \
                             '(name,email,telephone,address,password) ' \
                             'values(%s,%s,%s,%s,%s)'
                cursor = connection.cursor()
                cursor.execute(insert_sql, [name, email, telephone, address, password])
                success={'info': "success"}
                return HttpResponse(json.dumps(success), content_type="application/json")
    else:
        cf=CustomersForm()
        return HttpResponseRedirect('/static/register.html')

#登录
#登陆成功后的index1和index2页面的不同就在于右上角个人信息与投诉信息不同（分管理员的和顾客的）
@csrf_exempt
def login(request):
    LOG_DEBUG("登录系统")
    if request.method=='POST':     #POST！！
        cf=CustomersForm(request.POST)
        LOG_DEBUG(cf)
        mf=cf
        print(cf)
        if cf.is_valid() :
            name=cf.cleaned_data['name']
            password = cf.cleaned_data['password']
            id = Customers.objects.raw('select id '
                                        'from Customers '
                                        'where name=%s and password=%s',[name, password])
                                        
            id = [nameId.id for nameId in id] # 返回符合姓名和密码的顾客id
            if id:
                id=id[0]
            LOG_DEBUG(id)
            manager_id = Customers.objects.raw('select id '
                                               'from Managers '
                                               'where name=%s and password=%s', [name, password])
            LOG_DEBUG(manager_id)
            manager_id = [nameId.id for nameId in manager_id]   # 返回符合姓名和密码的管理员id
            if manager_id:
                manager_id=manager_id[0]

            if id:  # 顾客的匹配上了
                LOG_DEBUG("顾客登录")
                success = {'info': "success"}
                response = HttpResponse(json.dumps(success), content_type="application/json")
                response.set_cookie('id', id , 3600)  # cookies操作
                response.set_cookie('identity', "customer", 3600)  # cookies操作
                return response
            else:  # 顾客的没匹配上（要求manager和顾客不能重名）
                if manager_id:  # 管理员的匹配上了
                    LOG_DEBUG("管理员登录")
                    success = {'info': "success"}
                    response = HttpResponse(json.dumps(success), content_type="application/json")
                    response.set_cookie('id', manager_id, 3600)
                    response.set_cookie('identity', "manager", 3600)  # cookies操作
                    return response
                else:
                    fail = {'info': "failure"}
                    response = HttpResponse(json.dumps(fail), content_type="application/json")
                    response.delete_cookie('name')
                    return response  # 顾客和管理员都登录不成功就返回登录失败
    else:
        cf=CustomersForm()
        mf=cf
        return HttpResponseRedirect('/static/login.html')

@csrf_exempt
def logout(request):
    LOG_DEBUG("注销")
    if request.method=='GET':
        logout = {'info': "logout"}
        response = HttpResponse(json.dumps(logout), content_type="application/json")
        response.delete_cookie('id')
        return response


def getPrivilege(request):
    LOG_DEBUG("返回权限信息")
    PrivilegeReturn = {"user_type": "tourist"}
    '''
    name = request.COOKIES.get('name', '')  # 可能是顾客，可能是管理员
    if not name:
        PrivilegeReturn = {
            "user_type": "tourist",
            "id": 0
        }
        return HttpResponse(json.dumps(PrivilegeReturn), content_type="application/json")
    LOG_DEBUG(name)
    customer_id = Customers.objects.raw('select id '
                               'from Customers '
                               'where name = %s', [name])
    customer_id = [nameId.id for nameId in customer_id]  # 返回符合姓名的顾客id
    manager_id = Managers.objects.raw('select id '
                                      'from Managers '
                                      'where name like %s', [name])
    manager_id = [nameId.id for nameId in manager_id]'''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            customer_id=request.COOKIES.get('id', '')
            if customer_id:
                PrivilegeReturn = {
                    "user_type": "customer",
                    "id": customer_id
                }
        else:
            manager_id = request.COOKIES.get('id', '')
            if manager_id:
                PrivilegeReturn = {
                    "user_type": "manager",
                    "id": manager_id
                }
    else:
        PrivilegeReturn = {
            "user_type": "tourist",
            "id": 0
        }
        return HttpResponse(json.dumps(PrivilegeReturn), content_type="application/json")
    LOG_DEBUG(PrivilegeReturn)
    return HttpResponse(json.dumps(PrivilegeReturn), content_type="application/json")


#主页右上角个人信息展示
def customerInfoDisplay(request):
    LOG_DEBUG("展示个人信息")
    '''
    name = request.COOKIES.get('name', '')
    if not name:
        return HttpResponse(json.dumps({'name': ''}), content_type="application/json")
    LOG_DEBUG(name)
    id = Customers.objects.raw('select id '
                                'from Customers '
                                'where name=%s', [name])
              
    id = [nameId.id for nameId in id]  # 返回符合姓名和密码的顾客id
    manager_id = Customers.objects.raw('select id '
                                       'from Managers '
                                       'where name=%s ', [name])
    manager_id = [nameId.id for nameId in manager_id]    # 返回符合姓名和密码的管理员id'''
    customerInfoReturn = {"name": ""}
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            customer_id=request.COOKIES.get('id', '')
            if customer_id:
                name = Customers.objects.raw(
                    """
                    select *
                    from Customers
                    where id=%s;
                    """
                    , [customer_id])

                name = [nameId.name for nameId in name]  # 返回符合姓名和密码的顾客id
                print(name)
                customerInfoReturn = {
                    "id": customer_id,
                    "name": name
                }
        else:
            manager_id = request.COOKIES.get('id', '')
            if manager_id:
                name = Managers.objects.raw('select name,id '
                                             'from Managers '
                                             'where id=%s ', [manager_id])
                name = [nameId.name for nameId in name]
                customerInfoReturn = {
                    "id": manager_id,
                    "name": name
                }

    LOG_DEBUG(customerInfoReturn)
    return HttpResponse(json.dumps(customerInfoReturn), content_type="application/json")

#主页右上角个人最近投诉信息展示
def complaintDisplay(request):
    LOG_DEBUG("展示最新个人投诉信息")
    complaintReturn=[]
    complaints = ""
    '''
    name = request.COOKIES.get('name','') #可能是顾客，可能是管理员
    if not name:
        return HttpResponse(json.dumps(complaintReturn), content_type="application/json")
    LOG_DEBUG(name)
    id=Customers.objects.raw('select id '
                                      'from Customers '
                                      'where name = %s',[name])
    id = [nameId.id for nameId in id]  # 返回符合姓名的顾客id
    manager_id=Managers.objects.raw('select id '
                                     'from Managers '
                                     'where name like %s',[name])
    manager_id = [nameId.id for nameId in manager_id]'''
    id=''
    manager_id=''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
    if id:
        LOG_DEBUG("投诉展示顾客信息")
        sql='select text,submit_date,status,complaint_id ' \
            'from Complaints ' \
            'where customer_id=%s ' \
            'order by submit_date desc'
        complaints=Complaints.objects.raw(sql, [id])
        LOG_DEBUG(complaints)
    if manager_id:
        LOG_DEBUG("投诉展示管理员信息")
        sql = 'select text,submit_date,status,complaint_id ' \
              'from Complaints ' \
              'where manager_id=%s ' \
              'order by submit_date desc'
        complaints = Complaints.objects.raw(sql, [manager_id])
    for complaint in complaints:
        LOG_DEBUG(complaint)
        complaintReturn.append({'text': complaint.text,
                                'submit_date': complaint.submit_date.strftime('%Y-%m-%d'),
                                'status': complaint.status,
                                'complaint_id': complaint.complaint_id})
    LOG_DEBUG(complaintReturn)
    complaintReturn = json.dumps(complaintReturn)
    return HttpResponse(complaintReturn, content_type="application/json")



def getRecommendations(request):
    recom = [
        {
            "title": "MacBook Pro",
            "price": "￥8370",
            "pic_src": "/static/images/goods/MacBook_Pro.jpg"
        },
        {
            "title": "Beats_solo2",
            "price": "￥688",
            "pic_src": "/static/images/goods/Beats_solo2.jpg"
        },
        {
            "title": "Philips SPA4040b",
            "price": "￥549",
            "pic_src": "/static/images/goods/Philips_SPA4040b.jpg"
        },
        {
            "title": "Logitech G910",
            "price": "￥399",
            "pic_src": "/static/images/goods/Logitech_G910.jpg"
        },
        {
            "title": "AKG k550",
            "price": "￥1098",
            "pic_src": "/static/images/goods/AKG_k550.jpg"
        },
    ]
    return HttpResponse(json.dumps(recom), content_type="application/json")

def goodDisplay(request):
    LOG_DEBUG("展示商品")
    list = []
    somegoods = ""

    if request.method == 'GET':    #按类别搜索后的结果
        category = request.GET.get('category', "所有类别") #未选择时记为All
        # 未选择类别时自动显示所有商品信息
        if category == "所有类别" or not category:
            somegoods = Goods.objects.raw('select id,name,price,image_path,remain from Goods')
        else:
            sql = 'select id,name,price,image_path,remain ' \
                  'from Goods ' \
                  'where type like %s'
            somegoods = Goods.objects.raw(sql, [category])
            
    for somegood in somegoods:
        list.append({'good_id': somegood.good_id,
                     'name': somegood.name,
                     'price': somegood.price,
                     'image_path': somegood.image_path,
                     'remain': somegood.remain})

    goodReturn = json.dumps(list)  # 未选择类别时自动显示所有商品信息
    return HttpResponse(goodReturn, content_type="application/json")

#按照类别和关键词共同搜索后的结果（关键词是针对商品名字的）
def search(request):
    LOG_DEBUG("搜索商品")
    searchgoods = ""
    list = []
    print("222222222222",request.method)
    if request.method == 'GET':  #按类别搜索后的结果
        category = request.GET.get('category', "所有类别") #未选择时记为All
        keyword = request.GET.get('keyword', "")

        LOG_DEBUG("kw:" + keyword)

        if category == "所有类别" or not category:
            if(keyword==""):
                searchgoods = Goods.objects.raw('select id,name,price,image_path,remain from Goods')
            else:
                """
                sql='select id,name,price,image_path,remain ' \
                    'from Goods ' \
                    "where name REGEXP .%s.;" % keyword
                print(sql)
                searchgoods = Goods.objects.raw(sql)
                """
                searchgoods1 = Goods.objects.filter(name__iregex=keyword + '.')
                searchgoods2 = Goods.objects.filter(name__iregex='.' + keyword)
                searchgoods3 = Goods.objects.filter(name__iregex='.' + keyword + '.')
                searchgoods = searchgoods1 | searchgoods2 | searchgoods3
                print(searchgoods.query)
        else:
            if(keyword==""):
                searchgoods = Goods.objects.raw('select id,name,price,image_path,remain from Goods where type like %s',[category])
            else:
                '''
                sql = 'select id,name,price,image_path,remain ' \
                      'from Goods ' \
                      'where name like %%s% and type like %s' '''
                searchgoods1 = Goods.objects.filter(type=category, name__iregex=keyword + '.' )
                searchgoods2 = Goods.objects.filter(type=category, name__iregex='.'+ keyword)
                searchgoods3 = Goods.objects.filter(type=category, name__iregex='.'+ keyword + '.')
                searchgoods = searchgoods1 | searchgoods2 | searchgoods3
        for searchgood in searchgoods:
            list.append({'good_id': searchgood.good_id,
                         'name': searchgood.name,
                         'price': searchgood.price,
                         'image_path': searchgood.image_path,
                         'remain': searchgood.remain})
        
    searchReturn = json.dumps(list)  # 未选择类别时自动显示所有商品信息
    return HttpResponse(searchReturn, content_type="application/json")

#顾客对投诉信息的处理：
'''
1.在首页有最近投诉信息，点击其中一条（getcomplainEntry），可以查看这一系列投诉，并且可以追加投诉（addComplaint）
（以上操作在complaintEntry.html页面完成）需要前端的complaint_id与complaint_id,text返回
2.首页点击查看所有投诉（allComplaintEntry）,查看所有投诉，后端cookies获取customer_name
可以提交新的投诉（submitComplaint）,前端text返回
(以上操作在complaint.html页面完成)text返回
'''
#顾客的，点击首页投诉信息，查看这一条的信息（以及源头投诉的）
def getComplaintEntry(request):
    LOG_DEBUG("获取投诉信息")
    print(request.method)
    if(request.method == 'GET'):
        complaint_list=[]
        complaint_id = request.GET.get('complaint_id')
        complaint = Complaints.objects.raw('select * '
                                           'from Complaints '
                                           'where complaint_id=%s', [complaint_id])   #这一条投诉信息

        print(complaint_id)
        
        source_cmplt_id = [source_id.source_cmplt_id for source_id in complaint]
        print(source_cmplt_id)
        LOG_DEBUG(source_cmplt_id)
        if source_cmplt_id:
            source_cmplt_id = source_cmplt_id[0]
        else:
            source_cmplt_id = None
            
        if source_cmplt_id:  #是系列投诉
            complaint = Complaints.objects.raw('select * '
                                               'from Complaints '
                                               'where complaint_id=%s', [source_cmplt_id])

            for cpt in complaint:
                if cpt.proceed_date:
                    proceed_date=cpt.proceed_date.strftime('%Y-%m-%d')
                else:
                    proceed_date=''
                complaint_list.append({'text': cpt.text,
                                       'customer_id':cpt.customer_id,
                                       'complaint_id':cpt.complaint_id,
                                       'submit_date': str(cpt.submit_date.strftime('%Y-%m-%d')),
                                       'status': cpt.status,
                                       'proceed_date': proceed_date,
                                       'reply': cpt.reply})
                print('customer_id', cpt.customer_id)
            while complaint[0].follow_cmplt_id: #系列还没断
                complaint = Complaints.objects.raw('select * '
                                                   'from Complaints '
                                                   'where complaint_id=%s', [complaint[0].follow_cmplt_id])

                for cpt in complaint:
                    if cpt.proceed_date:
                        proceed_date = cpt.proceed_date.strftime('%Y-%m-%d')
                    else:
                        proceed_date = ''
                    print("date" + str(cpt.submit_date.strftime('%Y-%m-%d')))
                    complaint_list.append({'text': cpt.text,
                                           'customer_id': cpt.customer_id,
                                           'complaint_id': cpt.complaint_id,
                                           'submit_date': cpt.submit_date.strftime('%Y-%m-%d'),
                                           'status': cpt.status,
                                           'proceed_date': proceed_date,
                                           'reply': cpt.reply})
        else:
            for cpt in  complaint:
                print("date"+ str(cpt.submit_date.strftime('%Y-%m-%d')))
                complaint_list.append({'text': cpt.text,
                                       'customer_id': cpt.customer_id,
                                       'complaint_id': cpt.complaint_id,
                                       'submit_date': str(cpt.submit_date.strftime('%Y-%m-%d')),
                                       'status': cpt.status,
                                       'proceed_date': cpt.proceed_date.strftime('%Y-%m-%d'),
                                       'reply': cpt.reply})          #把相关投诉的信息存到了complaint_list里

        complaint_list = json.dumps(complaint_list)
        return HttpResponse(complaint_list, content_type="application/json")
#    else:
 #       return HttpResponseRedirect('/static/complaintEntry.html')

#查看一系列投诉后追加投诉
def addComplaint(request):
    LOG_DEBUG("追加投诉信息")
    complaint_id = request.POST.get('complaint_id', '')
    text=request.POST.get('text', '')
    if (complaint_id and text !=''):
        complaint = Complaints.objects.raw('select * '
                                         'from Complaints '
                                         'where complaint_id=%s ', [complaint_id]) #当前投诉

        source=complaint[0].source_cmplt_id
        print("source",source)
        for cpt in complaint:
            customer_id = cpt.customer_id
            manager_id = cpt.manager_id
            source_cmplt_id = cpt.source_cmplt_id
        submit_date = timezone.localtime(timezone.now())  #获取当前投诉信息
        next_id = max([oid['complaint_id'] for oid in Complaints.objects.values('complaint_id')] )+1
        update_sql = 'update Complaints ' \
                    'set follow_cmplt_id=%s ' \
                    'where complaint_id=%s'
        cursor=connection.cursor()
        cursor.execute(update_sql, [next_id, complaint_id])  #当前投诉信息的follow_cmplt给加上

        insert_sql='insert into Complaints ' \
                   '(complaint_id, customer_id, manager_id,source_cmplt_id,submit_date,text,status) ' \
                   'values(%s,%s,%s,%s,%s,%s,"wait")'
        cursor = connection.cursor()
        cursor.execute(insert_sql, [next_id, customer_id, manager_id, source, submit_date,text])  #给数据库添加新的信息
        success={'info': 'success'}
        return HttpResponse(json.dumps(success), content_type="application/json")
    else:
        fail = {'info': 'failure'}
        return HttpResponse(json.dumps(fail), content_type="application/json")

def allComplaintEntry(request):
    LOG_DEBUG("顾客查看自己的所有投诉")
    '''
    customer_name = request.COOKIES.get('name','')
    if customer_name:
        id = Customers.objects.raw('select id '
                                            'from Customers '
                                            'where name like %s', [customer_name])  # customer是{'id':..}
        id = [nameId.id for nameId in id]'''
    id = ''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
        if id:
            sql =\
                """
                select complaint_id, text,submit_date,status,proceed_date, reply
                from Complaints
                where customer_id=%s
                order by submit_date desc
                """
           # cursor = connection.cursor()
           # cursor.execute(sql, [id])
           #complaint_list = cursor.fetchone()
            complaint_list=Complaints.objects.raw(sql,[id])
            list=[]
            for cpt in complaint_list:
                if cpt.proceed_date:
                    proceed_date = cpt.proceed_date.strftime('%Y-%m-%d')
                else:
                    proceed_date = ''
                list.append({'text': cpt.text,
                             'complaint_id': cpt.complaint_id,
                             'submit_date': str(cpt.submit_date.strftime('%Y-%m-%d')),
                             'status': cpt.status,
                             'proceed_date': proceed_date,
                             'reply': cpt.reply})
            return HttpResponse(json.dumps(list), content_type="application/json")
 #   return HttpResponseRedirect('/static/complaint.html')


#提交投诉
def submitComplaint(request):
    LOG_DEBUG("提交投诉信息")
    if (request.method == 'POST'):
        text = request.POST.get('text', '')
        '''
        customer_name = request.COOKIES.get('name', '')
        if customer_name:
            id = Customers.objects.raw('select id '
                                                'from Customers '
                                                'where name like %s', [customer_name])#customer是{'id':..}
            id = [nameId.id for nameId in id]'''
        id=''
        identity = request.COOKIES.get('identity', '')
        if identity:
            if identity == "customer":
                id = request.COOKIES.get('id', '')
            else:
                manager_id = request.COOKIES.get('id', '')
            if id:
                try:
                    complaint_id = Complaints.objects.raw('select complaint_id from Complaints order by complaint_id desc')[0]
                    next_id = complaint_id.complaint_id + 1
                except:
                    next_id = 1

                manager_id = Managers.objects.raw('select id from Managers order by id desc')[0]
                manager_id = manager_id.manager_id   # 随机找一个管理员负责
                submit_date = timezone.now()
                insert_sql = 'insert into Complaints ' \
                             '(complaint_id,customer_id,manager_id,source_cmplt_id,submit_date,text,status) ' \
                             'values(%s,%s,%s,%s,%s,%s,"wait")'
                cursor = connection.cursor()
                cursor.execute(insert_sql, [next_id, id, manager_id, next_id, submit_date, text])  # 给数据库添加新的信息
                success = {'info': 'success'}
                return HttpResponse(json.dumps(success), content_type="application/json")
            else:
                fail = {'info': 'failure'}
                return HttpResponse(json.dumps(fail), content_type="application/json")

#管理员对投诉信息的处理：
'''
1.首页点击查看自己分配到的所有投诉（getComplaintWork）,查看所有投诉，cookies获取manager_name
点击其中一条（managerComplainEntry），可以查看这一条的一系列投诉,前端传回complaint_id
(以上操作在managerComplain.html页面完成)
2.写回复改状态(replyToComplaint)，前端POST过来回复
(在managerComplaintEntry.html页面完成)
'''
def getComplaintWork(request):
    LOG_DEBUG("管理员首页查看自己的所有投诉")
    '''
    manager_name = request.COOKIES.get('name', '')
    if manager_name:
        manager_id = Managers.objects.raw('select manager_id '
                                          'from Customers '
                                          'where name like %s', [manager_name])
        manager_id = [nameId.id for nameId in manager_id]'''
    id = ''
    manager_id=''
    complaint_list = []
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
        if manager_id:
            complaint_list=[]
            sql = 'select customer_id,text,submit_date,status,complaint_id ' \
                  'from Complaints ' \
                  'where manager_id=%s ' \
                  'order by submit_date desc '
            '''
            cursor = connection.cursor()
            cursor.execute(sql, [manager_id])
            temp_list = cursor.fetchone()'''
            temp_list=Complaints.objects.raw(sql, [manager_id])
            for complaint in temp_list:
                id=complaint.customer_id
                customer_name = Customers.objects.raw('select id,name from Customers where id=%s', [id])
                customer_name = customer_name[0].name
                complaint_list.append({'customer_id':id,
                                      'customer_name':customer_name,
                                      'text':complaint.text,
                                      'submit_date':complaint.submit_date.strftime('%Y-%m-%d'),
                                      'status':complaint.status,
                                      'complaint_id':complaint.complaint_id})

                print("complaint.complaint_id:", complaint.complaint_id)

    return HttpResponse(json.dumps(complaint_list), content_type="application/json")
#    return HttpResponseRedirect('/static/managerComplain.html')

#管理员点击一个投诉信息，只要有id就直接跳转到/static/managerComplaintEntry.html页面
#在/static/managerComplaintEntry.html页面再处理显示信息和回复问题
def managerComplaintEntry(request):
    LOG_DEBUG("管理员查看一条投诉信息")
    complaint_id=request.GET.get('complaint_id','')
    if complaint_id:
        return HttpResponseRedirect('/static/managerComplainEntry.html')

#这个页面显示投诉信息，可以接受回复消息
def replyToComplaint(request):
    LOG_DEBUG("接收回复信息，显示成功失败")
    complaint_id=request.POST.get('complaint_id', '') #接收到有效id后才跳转来的，所以不用判断
    text=request.POST.get('text','')
    complaint_list = []
    proceed_date = timezone.localtime(timezone.now())
    complaint = Complaints.objects.raw('select * '
                                       'from Complaints '
                                       'where complaint_id=%s', [complaint_id])  # 这一条投诉信息
    '''
    source_cmplt_id = [cpt.source_cmplt_id for cpt in complaint]
    if source_cmplt_id:  # 是系列投诉
        complaint = Complaints.objects.raw('select * '
                                           'from Complaints '
                                           'where complaint_id=%s', [source_cmplt_id[0]])
        for cpt in complaint:
            complaint_list.append({'text': cpt.text,
                                   'complaint_id': cpt.complaint_id,
                                   'submit_date': cpt.submit_date.strftime('%Y-%m-%d'),
                                   'status': cpt.status,
                                   'proceed_date': proceed_date.strftime('%Y-%m-%d'),
                                   'reply': cpt.reply})
        while complaint[0].follow_cmplt_id:  # 系列还没断
            for cpt in complaint:
                complaint_list.append({'complaint_id':cpt.complaint_id,
                                      'text': cpt.text,
                                       'submit_date': cpt.submit_date.strftime('%Y-%m-%d'),
                                       'status': cpt.status,
                                       'proceed_date': proceed_date.strftime('%Y-%m-%d'),
                                       'reply': cpt.reply})
                print("cpt.complaint_id",cpt.complaint_id)
            complaint = Complaints.objects.raw('select * '
                                           'from Complaints '
                                           'where complaint_id=%s', [complaint[0].follow_cmplt_id])
    else:
        for cpt in complaint:
            complaint_list.append({'text': cpt.text,
                                   'complaint_id': cpt.complaint_id,
                                   'submit_date': cpt.submit_date,
                                   'status': cpt.status,
                                   'proceed_date': proceed_date.strftime('%Y-%m-%d'),
                                   'reply': cpt.reply}) # 把相关投诉的信息存到了complaint_list里
                                                                                         '''
    if text:
        update_sql = 'update Complaints ' \
                     'set reply=%s, status="done" ' \
                     'where complaint_id=%s'
        cursor = connection.cursor()
        cursor.execute(update_sql, [text, complaint_id])
        success={'info':'success'}
        return HttpResponse(json.dumps(success), content_type="application/json")
    else:
        failure={'info': 'failure'}
        return HttpResponse(json.dumps(failure), content_type="application/json")


    
#顾客点击添加购物车，把商品填到Customers.temp_order对应的订单中去，且此订单的is_temp值是1
def addGood(request):
    LOG_DEBUG("加入购物车")
#    customer_name = request.COOKIES.get('name', '')
    good_id = request.GET.get('good_id', '')
    good_name = Customers.objects.raw('select name,id '
                                      'from Goods '
                                      'where id=%s ', [good_id])
    good_name = good_name[0].name
    LOG_DEBUG(good_name)
    '''
    if customer_name:
        id = Customers.objects.raw('select id '
                                            'from Customers '
                                            'where name like %s', [customer_name])
        customer_id = id[0].id'''
    id = ''
    manager_id = ''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
        LOG_DEBUG(id)
#        temp_order = Customers.objects.raw('select temp_order '
#                                           'from Customers '
#                                           'where name like %s', [customer_name])


        temp_order = Customers.objects.get(id=id).temp_order
        order_id = ""
        
        if temp_order :
            order_id = temp_order
        else:
            try:
                temp_order = max( [oid['order_id'] for oid in Orders.objects.values('order_id')] )+1
            except Exception as e:
                LOG_DEBUG(e)
                temp_order = 1
            order_id = temp_order
            try:
                manager_id = max([oid['id'] for oid in Managers.objects.values('id')] )
                manager_id = random.randint(1, manager_id)  # 随机找一个管理员负责
            except Exception as e:
                manager_id = 1

            update_sql = 'update Customers set temp_order=%s ' \
                         'where id = %s;'

            cursor = connection.cursor()
            cursor.execute(update_sql, [order_id, id])  # 商品填进去

            insert_sql = 'insert into Orders(' \
                         'order_id, is_temp, good_str, good_num, customer_id,manager_id,status) ' \
                         'values(%s, 1, %s, %s, %s, %s, "unpaid")'
            cursor = connection.cursor()
            cursor.execute(insert_sql, [order_id, good_name, "0", id, manager_id]) #新建了一个临时订单，即购物%车
#        order=Customers.objects.raw('select * from Orders where order_id like %s',[order_id])
        
        good_str = ""
        good_num = ""
        print("search order id:" + str(order_id))
        try:
            order = Orders.objects.get(order_id = order_id)
            good_str=order.good_str
            good_num=order.good_num
        except Exception as e:
            print("exception!!" + str(e))
            pass

        print(good_str)
        good_list=good_str.split(',')   #转化为列表了
        num_list=good_num.split(',')
        isin=0
        for i in range(len(good_list)):  #查看订单中有没有同样商品，有的话加进去
            if good_list[i] == good_name:
                isin=1
                break
        if isin == 0:
            good_list.append(good_name)
            num_list.append(str(1))  #新增商品
        else:
            num=int(num_list[i])+1
            num_list[i]=str(num)  #原来商品数量加1
        good_str=",".join(good_list)
        good_num=",".join(num_list)
        update_sql='update Orders set good_str=%s,good_num=%s' \
                   'where order_id=%s'
        cursor = connection.cursor()
        cursor.execute(update_sql,[good_str, good_num, order_id])  # 商品填进去
        success={'info': 'success'}
        return HttpResponse(json.dumps(success), content_type="application/json")
    else:
        fail = {'info': 'fail'}
        return HttpResponse(json.dumps(fail), content_type="application/json")


#顾客查看自己的所有订单
def orderEntry(request):
    LOG_DEBUG("顾客产看自己所有订单")
    '''
    customer_name = request.COOKIES.get('name', '')
    if customer_name:
        id = Customers.objects.raw('select id ' 
                                   'from Customers ' 
                                   'where name like %s ', [customer_name])
        id = [nameId.id for nameId in id]'''
    id = ''
    manager_id = ''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
        if id:
            order_list=[]
            sql = 'select order_id, good_str, good_num, status, submit_date ' \
                  'from Orders ' \
                  'where customer_id=%s and is_temp!=1 ' \
                  'order by submit_date desc '
            '''
            cursor = connection.cursor()
            cursor.execute(sql, [id])
            temp_list = cursor.fetchone()#此时是数组'''
            temp_list = Orders.objects.raw(sql, [id])
            print("order_id:",temp_list[0].customer_id)
            if temp_list:
                for temp in temp_list:
                    order_id = temp.order_id  # 待返回
                    good_names = temp.good_str  # 待返回
                    status = temp.status  # 待返回
                    submit_date = temp.submit_date  # 待返回

                    good_list = temp.good_str.split(',')  # 从这里开始算总金额
                    num_list = temp.good_num.split(',')
                    sum = 0
                    num_list = temp.good_num.split(',')

                    for j in range(len(num_list)):
                        num_list[j] = int(num_list[j])
                    for j in range(len(good_list)):
                        price = Customers.objects.raw('select id, price from Goods where name like %s', [good_list[j]])
                        price = price[0].price
                        sum = sum + price * num_list[j]  # 总金额是sum

                    order_list.append({'order_id': order_id,
                                       'good_names': good_list,
                                       'good_nums': num_list,
                                       'total': sum,
                                       'status': status,
                                       'submit_date': submit_date.strftime('%Y-%m-%d')})
            else:
                order_list = []
            print(order_list)
            return HttpResponse(json.dumps(order_list), content_type="application/json")
#    return HttpResponseRedirect('/static/orders.html')

#顾客查看自己的购物车（Customers.temp_order指引的临时订单）
def getShoppingList(request):
    LOG_DEBUG("查看购物车")
#    customer_name = request.COOKIES.get('name', '')
    id = ''
    manager_id = ''
    shop_list = []
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
    if id:
        temp_order = Customers.objects.raw('select id, temp_order from Customers where id = %s', [id])
        temp_order = temp_order[0].temp_order
        if (temp_order):
            order=Orders.objects.raw('select * from Orders where order_id=%s', [temp_order])
            good_num=order[0].good_num
            good_str=order[0].good_str
            good_list=good_str.split(",")
            num_list=good_num.split(",")
            print(good_list)
            for i in range(len(good_list)):
                good = Goods.objects.raw('select * from Goods where name like %s', [good_list[i]])
                shop_list.append({'good_id': good[0].good_id,
                                  'name': good[0].name,
                                  'good_num': int(num_list[i]),
                                  'price': good[0].price,
                                  'image_path': good[0].image_path,
                                  'remain': good[0].remain})

    return HttpResponse(json.dumps(shop_list), content_type="application/json")
 #   return HttpResponseRedirect('/static/shoppingList.html')

#顾客提交订单（Customers.temp_order指引的临时订单变成正式订单，临时标志消失）
def submitShoppingList(request):
    LOG_DEBUG("顾客提交订单")
    id = ''
    manager_id = ''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
    if id:
        temp_order = Customers.objects.raw('select id, temp_order from Customers where id = %s', [id])
        temp_order = temp_order[0].temp_order
        if(temp_order):
            submit_date = timezone.localtime(timezone.now())
            print(submit_date)
            update_sql='update Orders set is_temp=0, submit_date=%s ' \
                       'where order_id=%s '
            cursor = connection.cursor()
            cursor.execute(update_sql, [submit_date, temp_order])
            update_sql = 'update Customers set temp_order=0 where id=%s '
            cursor = connection.cursor()
            cursor.execute(update_sql, [id])
            success = {'info': 'success'}
            return HttpResponse(json.dumps(success), content_type="application/json")
        else:
            fail = {'info': 'fail'}
            return HttpResponse(json.dumps(fail), content_type="application/json")

#员工查看自己被分到的订单
def getOrderWork(request):
    LOG_DEBUG("管理员查看自己所有订单")
    '''
    manager_name = request.COOKIES.get('name', '')
    if manager_name:
        manager_id = Managers.objects.raw('select manager_id from Customers where name like %s',[manager_name])
        manager_id = manager_id[0].manager_id'''
    id = ''
    manager_id = ''
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            id = request.COOKIES.get('id', '')
        else:
            manager_id = request.COOKIES.get('id', '')
        if manager_id:
            order_list=[]
            sql = 'select order_id,customer_id, good_str,good_num,status,submit_date ' \
                  'from Orders ' \
                  'where manager_id=%s and is_temp!=1 ' \
                  'order by submit_date desc '
            '''
            cursor = connection.cursor()
            cursor.execute(sql, [manager_id])
            temp_list = cursor.fetchall()#此时是数组
            temp_list=list(temp_list)'''
            temp_list=Orders.objects.raw(sql, [manager_id])
            for temp in temp_list:
                id = temp.customer_id  # 待返回
                customer_name = Customers.objects.raw('select id, name from Customers where id=%s ', [id])
                customer_name = customer_name[0].name  # 待返回
                order_id = temp.order_id  # 待返回
                good_names = temp.good_str  # 待返回
                good_nums = temp.good_num
                status = temp.status  # 待返回
                submit_date = temp.submit_date  # 待返回
                '''
                for i in range(len(temp_list)):
                temp_list[i] = list(temp_list[i])
                print(temp_list[i])
                id=temp_list[i].[0]  #待返回
                customer_name = Customers.objects.raw('select id, name from Customers where id=%s ', [id])
                customer_name = customer_name[0].customer_name #待返回
                order_id=temp_list[i].order_id    #待返回
                good_names=temp_list[i].good_str  #待返回
                good_nums=temp_list[i].good_num
                status=temp_list[i].status #待返回
                submit_date = temp_list[i].submit_date #待返回'''

                good_list=temp.good_str.split(',')   #从这里开始算总金额
                print("good_list",good_list)
                num_list=temp.good_num.split(',')
                for j in range(len(num_list)):
                    num_list[j]=int(num_list[j])
                print(num_list)
                sum=0
                for j in range(len(good_list)):
                    price = Goods.objects.raw('select id, price from Goods where name like %s',[good_list[j]])
                    print("price ",price)
                    price=price[0].price
                    sum = sum + price * num_list[j]  #总金额是sum
                print("sum",sum)
                order_list.append({'customer_id': id,
                                   'customer_name':customer_name,
                                   'order_id':order_id,
                                   'good_names':good_list,
                                   'good_nums':num_list,
                                   'total':sum,
                                   'status':status,
                                   'submit_date':submit_date.strftime('%Y-%m-%d')})
            return HttpResponse(json.dumps(order_list), content_type="application/json")
#    return HttpResponseRedirect('/static/managerOrder.html')

def changeOrderStatus(request):
    LOG_DEBUG("管理员修改订单状态")
    order_id=request.GET.get('order_id', '')
    target_status=request.GET.get('target_status', '')
    if (order_id and target_status):
        update_sql = 'update Orders set status=%s' \
                     'where order_id=%s'
        cursor = connection.cursor()
        cursor.execute(update_sql, [target_status, order_id])
        success = {'info': 'success'}
        return HttpResponse(json.dumps(success), content_type="application/json")
    else:
        fail = {'info': 'fail'}
        return HttpResponse(json.dumps(fail), content_type="application/json")

def editCustomerInfo(request):
    LOG_DEBUG("顾客修改个人信息")
    new_username=request.GET.get('username', '')
    new_address=request.GET.get('address', '')
    new_telephone=request.GET.get('telephone', '')
    new_email=request.GET.get('email', '')
    identity = request.COOKIES.get('identity', '')
    if identity:
        if identity == "customer":
            customer_id = request.COOKIES.get('id', '')
            if customer_id:
                update_sql='update Customers set name=%s, address=%s, telephone=%s, email=%s where id = %s '
                cursor = connection.cursor()
                cursor.execute(update_sql, [new_username, new_address, new_telephone, new_email, customer_id])
                success = {'info': 'success'}
                return HttpResponse(json.dumps(success), content_type="application/json")
            else:
                fail = {'info': 'fail'}
                return HttpResponse(json.dumps(fail), content_type="application/json")
    fail = {'info': 'fail'}
    return HttpResponse(json.dumps(fail), content_type="application/json")

def getCustomerInfo(request):
    LOG_DEBUG("取得个人信息")
    identity = request.COOKIES.get('identity', '')
    CustomerInfoReturn = {}
    if identity:
        if identity == "customer":
            customer_id = request.COOKIES.get('id', '')
            if customer_id:
                sql='select * from Customers where id=%s '
                customer = Customers.objects.raw(sql, [customer_id])
                CustomerInfoReturn = {'username':customer[0].name,
                                      'address':customer[0].address,
                                      'telephone':customer[0].telephone,
                                      'email':customer[0].email}
                return HttpResponse(json.dumps(CustomerInfoReturn), content_type="application/json")

'''
@csrf_exempt
def getPrivilege(request):
    return HttpResponse(json.dumps({'user_type': "manager"}), content_type="application/json")'''


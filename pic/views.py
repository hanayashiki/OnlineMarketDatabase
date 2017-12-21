import json
from django.shortcuts import render, HttpResponse

# Create your views here.

def get_recommendations(request):
    recom = [
        {
            "title": "A",
            "price": "10$",
            "pic_src": "/static/shojo.jpg"
        },
        {
            "title": "B",
            "price": "20$",
            "pic_src": "/static/shojo.jpg"
        },
        {
            "title": "C",
            "price": "30$",
            "pic_src": "/static/shojo.jpg"
        },
        {
            "title": "D",
            "price": "40$",
            "pic_src": "/static/shojo.jpg"
        },
        {
            "title": "E",
            "price": "50$",
            "pic_src": "/static/shojo.jpg"
        },
    ]
    return HttpResponse(json.dumps(recom), content_type="application/json")


def get_customer_info_display(request):
    recom = {
        "customer_id": 1234,
        "name": "李剑锋"
    }
    return HttpResponse(json.dumps(recom), content_type="application/json")


def get_complaint_display(request):
    recom = [
        {
            "text": "工商部门也在此提醒，消费者购买供暖设备应选择品牌可靠、售后服务网点多、信誉良好的经销商；购买前要仔细了解商品配置情况与售后服务承诺，不要轻信销售人员的口头介绍与承诺；不要贪图便宜选择质次的产品。要仔细检查产品有无厂名、厂址、合格证书；使用电器类供暖设备要严格按照产品说明书规定使用。不要将其周围放置易燃物品，以免引起火灾。使用后做到“人走断电”。",
            "submit_date": "2017/12/20",
            "status": "wait",
            "complaint_id": 10221
        },
        {
            "text": "据工商部门介绍，随着气温逐渐走低，近期“12315”、“96315”两条热线陆续接到有关购买供暖设备引发的消费投诉，根据投诉内容分析，供暖设备引发的投诉主要存在三种情况，一是保修期内出现不制热、供暖效果不佳、噪音大等方面的质量问题；二是商家以无货、送货人手不足为由未按承诺时间送货；三是经营者宣传供暖设备时夸大宣传其功能。",
            "submit_date": "2017/11/18",
            "status": "done",
            "complaint_id": 9223
        },
        {
            "text": "放心,只要你在考试完了没点取消成绩,成绩肯定是有的,报名网站那显示我觉得是一直都有错",
            "submit_date": "2017/11/17",
            "status": "done",
            "complaint_id": 9098
        },
        {
            "text": "报名网站那显示我觉得是一直都有错",
            "submit_date": "2017/11/17",
            "status": "done",
            "complaint_id": 9099
        },
        {
            "text": "近期“12315”、“96315”两条热线陆续接",
            "submit_date": "2017/11/17",
            "status": "done",
            "complaint_id": 9099
        },
        {
            "text": "放心,只要你在考试完了没点取消成绩,成绩肯定是有的,报名网站那显示我觉得是一直都有错",
            "submit_date": "2017/11/17",
            "status": "done",
            "complaint_id": 9098
        },
    ]

    return HttpResponse(json.dumps(recom), content_type="application/json")


def get_good_display(request):
    recom =\
    [
        {
            "good_id": 114514,
            "name": "DDF战甲",
            "price": 233,
            "image_path": "/static/images/cont/main_img1.jpg",
            "remain": 114,
        },
        {
            "good_id": 115514,
            "name": "假发",
            "price": 15,
            "image_path": "/static/images/cont/main_img2.jpg",
            "remain": 24,
        },
        {
            "good_id": 112514,
            "name": "水手服",
            "price": 12,
            "image_path": "/static/images/cont/main_img3.jpg",
            "remain": 28,
        },
        {
            "good_id": 114514,
            "name": "DDF战甲",
            "price": 233,
            "image_path": "/static/images/cont/main_img1.jpg",
            "remain": 114,
        },
        {
            "good_id": 115514,
            "name": "假发",
            "price": 15,
            "image_path": "/static/images/cont/main_img2.jpg",
            "remain": 24,
        },
        {
            "good_id": 112514,
            "name": "水手服",
            "price": 12,
            "image_path": "/static/images/cont/main_img3.jpg",
            "remain": 28,
        },
        {
            "good_id": 114514,
            "name": "DDF战甲",
            "price": 233,
            "image_path": "/static/images/cont/main_img1.jpg",
            "remain": 114,
        },
        {
            "good_id": 115514,
            "name": "假发",
            "price": 15,
            "image_path": "/static/images/cont/main_img2.jpg",
            "remain": 24,
        },
        {
            "good_id": 112514,
            "name": "水手服",
            "price": 12,
            "image_path": "/static/images/cont/main_img3.jpg",
            "remain": 28,
        },
    ]

    if request.GET.get("category") == "女装":
        recom.append({
            "good_id": 112514,
            "name": "黑框眼镜",
            "price": 12,
            "image_path": "/static/images/cont/main_img3.jpg",
            "remain": 28,
        })

    return HttpResponse(json.dumps(recom), content_type="application/json")


def response_add_good(request):
    return HttpResponse(json.dumps({"info": "success"}), content_type="application/json")
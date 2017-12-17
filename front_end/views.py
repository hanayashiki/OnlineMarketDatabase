from django.shortcuts import render

# Create your views here.

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
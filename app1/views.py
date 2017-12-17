from django.shortcuts import render
from app1 import models
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.template.loader import get_template
from django.template import loader, RequestContext
from django.http import HttpResponse

# Create your views here.
def index(request,cat_id=0):
    all_products=None
    if cat_id > 0:
        try:
            category=models.goods.type.get(id=cat_id)
        except:
            category=None
        if category is not None:
            all_products=models.goods.objects.filter(category=type)
    if all_products is None:
        all_products=models.goods.objects.all()

    paginator=Paginator(all_products,4)
    p=request.GET.get('p')
    try:
        products=paginator.page(p)
    except PageNotAnInteger:
        products=paginator.page(1)
    except EmptyPage:
        products=paginator.page(paginator.num_pages)

    template=get_template('index.html')
    request_context=RequestContext(request)
    request_context.push(locals())
    html=template.render(request_context)
    all_categories=models.goods.type.all()
    return HttpResponse(html)
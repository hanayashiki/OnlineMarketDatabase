"""jq_django_test URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from pic.views import get_recommendations, get_customer_info_display,\
    get_complaint_display, get_good_display, response_add_good,\
    response_search

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getRecommendations/', get_recommendations),
    url(r'^customerInfoDisplay/', get_customer_info_display),
    url(r'^complaintDisplay/', get_complaint_display),
    url(r'^goodDisplay/', get_good_display),
    url(r'^addGood/', response_add_good),
    url(r'^search/', response_search)
]

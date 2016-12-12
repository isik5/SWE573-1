"""nutritrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'usda'
urlpatterns = [
    url(r'^$', views.foodsearch, name='foodsearch'),
    url(r'^search/$', views.searchrequest, name='search_request'),
    url(r'^details/$', views.details, name='details'),
    url(r'^eat/$', views.eat, name='eat'),
    url(r'^activity/$', views.activitysearch, name='activity'),
    url(r'^activity_details/$', views.activity_details, name='activity_details'),
    url(r'^activity_search_request/$', views.searchactivityrequest, name='search_activity_request'),
    url(r'^activity_apply/$', views.activity_apply, name='activity_apply'),

]

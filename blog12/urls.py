"""blog12 URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from django.http import  HttpRequest,HttpResponse,JsonResponse
from django.shortcuts import  render
import user.urls
import datetime
def index(request:HttpRequest):
    mydict ={
        'a':100,
        'b':0,
        'c':list(range(1,10)),
        'd':'abc',
        'date':datetime.datetime.now()
    }
    return render(request,'index.html',{'mydict':mydict})

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index',index),
    url(r'^user/',include('user.urls')),
    url(r'^post/',include('post.urls'))
]

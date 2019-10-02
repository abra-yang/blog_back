from django.shortcuts import render
from django.http import HttpRequest,JsonResponse,HttpResponseBadRequest
# Create your views here.
from user.views import auth_cert
import simplejson
from .models import Content,Post
import datetime
import math

@auth_cert
def pub(request:HttpRequest):
    payload = simplejson.loads(request.body)
    print(request.user.id)
    try:
        post = Post()
        content = Content()
        post.title = payload['title']
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.author = request.user
        post.save()
        content.content = payload['content']
        content.post = post
        content.save()
        return JsonResponse({'post_id':post.id})
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('文章未发布')


def get(request,id):
    try:
        id = int(id)
        print(id)
        post = Post.objects.filter(pk=id).first()
        if not post:
            return HttpResponseBadRequest('文章不存在')
        return JsonResponse({
            'post':{
                'post_id':post.id,
                'auther':post.author.name,
                'auther_id':post.author.id,
                'content':post.content.content,
                'postdate':post.postdate,
                'title':post.title
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('error')

def auth_input(d,name,default,auth_fun):
    try:
        s = int(d.get(name,default))
        s = auth_fun(s,default)
    except:
        s = default
    return s

def getall(request:HttpRequest):
    page = auth_input(request.GET,'page',1,lambda x,y: x if x>0 else y)
    size = auth_input(request.GET,'size',20,lambda x,y: x if x>0 and x <101 else y)
    try:
        posts = Post.objects.order_by('-id')  #这是返回的一个set。
        count = posts.count()      #博客数量
        print(posts.query, '~~~')  # 打印查询语句
        pagesize = math.ceil(count / size)
        start = (page - 1) * size
        posts = posts[start:start+size]
        return JsonResponse({'post':[{'postid':post.id,'post_tilte':post.title} for post in posts],
                             'pageinfo':{
                                 'page':page,
                                 'pagesize':pagesize,
                                 'count':count,
                                 'size':size}
                             })
    except:
        return HttpResponseBadRequest('found error')
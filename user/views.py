from django.http import JsonResponse,HttpRequest,HttpResponseBadRequest,HttpResponse
import simplejson
from .models import User
import bcrypt
import jwt
from django.conf import settings
import datetime
from django.shortcuts import render
# Create your views here.

def gen(userid):
    return jwt.encode({
        'user_id':userid ,
        'exp':int(datetime.datetime.now().timestamp()+360)
    },settings.SECRET_KEY,'HS256')

def reg(request:HttpRequest):
    data = simplejson.loads(request.body)
    try:
        email = data['email']
        query = User.objects.filter(email=email)#懒查询，不需要数据不会进行查询。
        if  query.first():
            return HttpResponseBadRequest('邮箱已注册')#如果非空即返回badrequest,状态码400系列。
        user = User()#如果此邮箱未注册，则继续执行，
        user.name = data['name']
        user.email = email
        passwd = data['password'].encode()
        try:
            user.passwd = bcrypt.hashpw(passwd,bcrypt.gensalt())
            user.save()
            return JsonResponse({'user_id':user.id})
        except :
            raise
    except Exception as e:
        return HttpResponseBadRequest('参数错误')#第一个语句块如果用户输入空数据，取不到值就会异常捕获


def auth_cert(fn):
    def _wrapper(request):
        payload = request.META.get('HTTP_JWT')
        try:
            if not payload:
                return HttpResponseBadRequest('身份认证失败，重新登录',status=401)
            try:
                payload_encode = jwt.decode(payload,settings.SECRET_KEY,'HS256')
                user_id = payload_encode['user_id']

                user = User.objects.filter(pk = user_id).get()
                request.user = user
                ret = fn(request)
                return  ret
            except jwt.ExpiredSignatureError as e:
                print(e)
                return HttpResponseBadRequest('用户过期')
        except Exception as e:
            print(e, '!!!')
            return HttpResponseBadRequest('用户验证失败')
    return _wrapper


def login(request:HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        password = payload['password']
        user = User.objects.filter(email=email).first()
        if bcrypt.checkpw(password.encode(),user.passwd.encode()):
            token = gen(user.id).decode()
            res = JsonResponse({
                'user':
                {'user':user.name,
                'email':user.email,
                'user_id':user.id},
                'token':token
            })
            res.set_cookie('JWT',token)
            return res
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('登录失败')


@auth_cert
def show(request:HttpRequest):
    return JsonResponse({'show':'test'})

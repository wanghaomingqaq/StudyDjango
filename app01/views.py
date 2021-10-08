from django.shortcuts import redirect, HttpResponse, render
from app01 import models
from app01.myclass import Weibo, Hupu, Twitter,Qidian,Cat,Jlu
from django.utils.safestring import mark_safe
from markdown import markdown
import time
import json



def hupu(request):
    my = models.Login.objects.get(username='haoming')
    coin_num = int(my.coin_num)
    dio_num = int(my.dio_num)
    res = {"coin_num":coin_num,"dio_num":dio_num}
    if request.method=="POST":
        coin = request.POST.get('coin')
        dio = request.POST.get('dio')
        my.coin_num = coin
        my.dio_num = dio
        my.save()
    return HttpResponse(json.dumps(res), content_type='application/json')
def login(request):
    if request.method == "POST":
        user = request.POST.get('username')
        password = request.POST.get('password')
        print(user, password)
        user_obj = models.Login.objects.filter(username=user).first()
        if user_obj:
            if password == user_obj.password:
                res = True
                return HttpResponse(json.dumps(res), content_type='application/json')

            else:
                return HttpResponse("PasswordError")
        else:
            return HttpResponse("UserNotFound")

def register(requset):
    if requset.method == "POST":
        username = requset.POST.get('username')
        email = requset.POST.get('email')
        password = requset.POST.get('password')
        res = models.Login.objects.create(username=username, email=email, password=password)
        return redirect('/login/')
    return render(requset, 'index.html')


def home(request):
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime, type(localtime))
    xingqi = localtime[:3]
    month = localtime[4:7]
    day = localtime[8:10]
    times = localtime[11:19]
    years = localtime[20:]
    queery = models.Jilin.objects.all()
    for que in queery:
        que.title = que.title.replace('&ensp', '')
        que.title = que.title.replace('[doge]', '')
        que.title = que.title[:30] + '...'
    return render(request, 'home.html', locals())


def qidian_refresh(request):
    models.QiDian.objects.all().delete()
    Qidian().qidian()
    print('refresh')
    return redirect('/qidian/')


def qidian(request):

    localtime = time.asctime(time.localtime(time.time()))
    print(localtime, type(localtime))
    xingqi = localtime[:3]
    month = localtime[4:7]
    day = localtime[8:10]
    times = localtime[11:19]
    years = localtime[20:]
    queery = models.Jilin.objects.all()
    for que in queery:
   #     que.content = mark_safe(que.content)
        que.title = que.title.replace('&ensp', '')
        que.title = que.title.replace('[doge]', '')
        que.title = que.title[:30] + '...'
    all = models.QiDian.objects.all()
    return render(request, 'qidian.html', locals())


def twitter(request):
    queery = models.Jilin.objects.all()
    a = Twitter().twitter('')
    return render(request, 'twitter.html', locals())


def weibo_net(request):
    queery = models.Jilin.objects.all()
    for que in queery:
 #       que.content = mark_safe(que.content)
        que.title = que.title.replace('&ensp', '')
        que.title = que.title.replace('[doge]', '')
        que.title = que.title[:30] + '...'

    return render(request, 'home.html', locals())


def cat(request):
    my = models.Login.objects.get(username='haoming')
    dio_num = int(my.dio_num)
    if request.method=="POST":
        dio = request.POST.get('dio')
        my.coin_num = dio
        my.save()

    return HttpResponse(json.dumps(dio_num), content_type='application/json')


def write(request):
    if request.method=="POST":
        contents = request.POST.get('contents')
        print(contents,'sadfasfd')
        return redirect('/home')
    return render(request,'views.html',locals())


def jlu_new(request):
    Jlu().jlu()
    return redirect('/jlu/')
def jlu(request):
    queery = models.Jilin.objects.all()
    return render(request,'jlu.html',locals())


def article(request,article_id):
    note = models.Article.objects.get(id=int(article_id))
    note.content = markdown(note.content,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])

    return render(request,'article.html',locals())

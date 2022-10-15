from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *

# Create your views here.

def index_view(request):
    value=request.COOKIES.get('user','')
    try:
        name=merchant.objects.get(username=value).name
    except:
        pass
    return render(request,"index.html",locals())

def shoplist_view(request):
    value=request.COOKIES.get('user','')
    try:
        name=merchant.objects.get(username=value).name
    except:
        pass
    shops=shop.objects.all()
    return render(request,"shoplist.html",locals())

def shopdetail_view(request,_id):
    value=request.COOKIES.get('user','')
    try:
        name=merchant.objects.get(username=value).name
    except:
        pass
    goods=shop.objects.get(id=_id).goods_set.all()
    return render(request,'shopdetail.html',locals())

def login_view(request):
    if request.method=='GET':
        value=request.COOKIES.get('user','')
        try:
            name=merchant.objects.get(username=value).name
        except:
            pass
        return render(request,'login.html',locals())
    elif request.method=='POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        try:
            mer=merchant.objects.get(username = uname)
        except:
            return render(request,'login.html')
        if mer.password==pwd:
            resp=HttpResponseRedirect('/login')
            resp.set_cookie('user',mer.username)
            return resp
        else:
            return render(request,'login.html')

def manage_view(request):
    value=request.COOKIES.get('user','')
    if value=='':
        return HttpResponseRedirect('/login')
    else:
        mer=merchant.objects.get(username=value)
        return render(request,'userinfo.html',locals())

def myshop_view(request):
    value=request.COOKIES.get('user','')
    if value=='':
        return HttpResponseRedirect('/login')
    else:
        mer=merchant.objects.get(username=value)
        shops=mer.shop_set.all()
        return render(request,'usershop.html',locals())

def charge_view(request):
    if request.method=='GET':
        value=request.COOKIES.get('user','')
        if value=='':
            return HttpResponseRedirect('/login')
        else:
            mer=merchant.objects.get(username=value)
            shops=mer.shop_set.all()
            money=0
            for shop in shops:
                money+=shop.type.paywater.money+shop.type.payelec.money+shop.market.rent.price
            return render(request,'charge.html',locals())
    elif request.method=='POST':
        value=request.COOKIES.get('user','')
        mer=merchant.objects.get(username=value)
        charge=int(request.POST['money'])
        mer.balance+=charge
        mer.save()
        return HttpResponseRedirect('userinfo')

def rent_view(request):
    if request.method=='GET':
        value=request.COOKIES.get('user','')
        if value=='':
            return HttpResponseRedirect('/login')
        try:
            name=merchant.objects.get(username=value).name
        except:
            pass
        try: 
            id=int(request.GET['shop_id'])
        except:
            value=request.COOKIES.get('user','')
            try:
                name=merchant.objects.get(username=value).name
            except:
                pass
            shops=market.objects.filter(is_rented=False)
            return render(request,'rent.html',locals())
        return render(request,'rent_add.html',locals())
    elif request.method=='POST':
        _type=request.POST['type']
        _name=request.POST['name']
        id=int(request.GET['shop_id'])
        _market=market.objects.get(id=id)
        _market.is_rented=True
        _market.save()
        t=type.objects.get(typename=_type)
        value=request.COOKIES.get('user','')
        m=merchant.objects.get(username=value)
        shop.objects.create(name=_name,market=_market,merchant=m,type=t)
        return HttpResponseRedirect("myshop")
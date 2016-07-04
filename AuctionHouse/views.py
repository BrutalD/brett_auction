# -*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from .models import *
from .forms import *
# Create your views here.


def index(request):
    user_name = request.COOKIES.get('username', '')
    return render_to_response('index.html', {'user_name':user_name})
def register(request):
    print('POST')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_user = User(**user_form.cleaned_data)
            new_user.save()
            return render_to_response('register/success.html',
                                      {'username':user_form.cleaned_data['user_name']})
    else:
        user_form = UserForm()
    return render_to_response('register/register.html',
                              {'uf':user_form},
                              context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        user_form = LoginUserForm(request.POST)
        if user_form.is_valid():
            name_or_email = user_form.cleaned_data['name_or_email']
            password = user_form.cleaned_data['password']
            user = User.objects.filter(
                Q(user_name=name_or_email) | Q(email=name_or_email),
                Q(password=password)
            )
            if user:
                # print("User Confirmed")
                # print(user)
                response = HttpResponseRedirect('/',
                                                {'username':user[0].user_name})
                response.set_cookie('username', user[0].user_name, 3600)
                return response
                # return render_to_response('login/success.html',
                #                           {'username':user[0].user_name})
            else:
                return HttpResponseRedirect('/login/')
    else:
        user_form = LoginUserForm()
    return render_to_response('login/login.html',
                              {'uf':user_form},
                              context_instance=RequestContext(request))


# 用户能看到的自身状态
def user(request):
    pass

# 注意，一个用户是不能看其他用户的购物车的。
# 所以，不需要在购物车之前指明用户
# 而是应该根据session和cookie判断当前登陆的用户
# 订单等等同理
def orders(request):
    pass

def bids(request):
    pass

def orders_unpaid(request):
    pass

def orders_unsent(request):
    pass

def orders_unconfirmed(request):
    pass

def cart(request):
    pass

def market(request):
    pass


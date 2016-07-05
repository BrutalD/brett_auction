# -*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from .models import *
from .forms import *
from .utils import *
# Create your views here.


def index(request):
    user_name = get_current_user(request)
    return render_to_response('index.html', {'user_name':user_name})

# 用户注册
def register(request):
    # print('POST')

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
                response.set_cookie('user_name', user[0].user_name, 3600)
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
def user(request, user_name):

    # 获取当前登陆的用户
    current_user = get_current_user(request)

    # 如果是当前登陆的用户在查看自身的状态
    if current_user == user_name:
        user_status = User.objects.filter(user_name=user_name)[0]
        if request.method == 'POST':
            # request.POST对象是一个QueryDict类型的对象，
            # 是一个单键可能对应多值的字典（实际上就是值都是包含在列表中的的）
            # 兼容字典的绝大多数方法
            # QueryDict.items()返回的值依然是单值（是通过__getitem__这个单值逻辑实现的）
            update_user_status = request.POST
            tmp_user_form = ShowUserForm(request.POST, request.FILES)
            if tmp_user_form.is_valid():
                for key, value in tmp_user_form.cleaned_data.items():
                    if value == '':
                        value = None
                    if hasattr(user_status, key):
                        setattr(user_status, key, value)
            # for key, value in update_user_status.items():
            #     # 如果form提交的时候文本框中没有值，那么value为''
            #     # 在数据库中存入一个空字符串是不合理的，也有可能出错（例如日期）
            #     # 需要转化成null，即Python中的None
            #     if value == '':
            #         value = None
            #     # 如果User对象没有这个属性，就不要更改这个属性
            #     if hasattr(user_status, key):
            #         setattr(user_status, key, value)
            # 真正地更改用户信息
            user_status.save()

        show_user_status = ShowUserForm(initial=user_status.__dict__, )
        return render_to_response('people/self.html',
                                  {'uf':show_user_status},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('people/other.html',
                                   context_instance=RequestContext(request))



# 注意，一个用户是不能看其他用户的购物车的。
# 所以，不需要在购物车之前指明用户
# 而是应该根据session和cookie判断当前登陆的用户
# 订单等等同理
def orders(request):
    current_user = get_current_user(request)
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


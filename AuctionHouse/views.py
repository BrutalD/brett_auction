# -*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import *
from django.core.exceptions import *
from django.db.models import Q
from .models import *
from .forms import *
from .utils import *
# Create your views here.

def pay(request):
    pass

def index(request):
    #user_name = get_current_user(request)
    # categories = Category.objects.all()
    # return render(request, 'index.html', {'user_name':user_name})
    return market(request)

# 用户注册
# def register(request):
#     # print('POST')
#     current_user = get_current_user(request)
#     try:
#         user = User.objects.get(user_name=current_user)
#     except ObjectDoesNotExist as e:
#         user = None
#
#     if request.method == 'POST':
#         if request.POST.has_key('login'):
#             user_form = RegisterUserForm(request.POST)
#             if user_form.is_valid():
#                 user_form.save()
#                 return HttpResponseRedirect('/market')
#         else:
#
#
#     return render(request,
#                   'login.html',
#                   {'current_user': user})

def login_register(request):

    current_user = get_current_user(request)
    try:
        user_obj = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        user_obj = None

    context = {'current_user': user_obj}

    if request.method == 'POST':
        if 'login' in request.POST:
            user_form = LoginUserForm(request.POST)
            if user_form.is_valid():
                name_or_email = user_form.cleaned_data['login_name_email']
                password = user_form.cleaned_data['login_password']
                try:
                    user = User.objects.get(
                    Q(user_name=name_or_email) | Q(email=name_or_email),
                    Q(password=password)
                    )
                    response = HttpResponseRedirect('/')
                    response.set_cookie('user_name', user.user_name, 3600)
                    return response
                except ObjectDoesNotExist as e:
                    context['error_msg'] = '无效的用户名或密码'
                    return render(request, 'login.html',context)
            else:
                context['error_msg'] = '数据格式错误'
                return render(request, 'login.html', context)
        else:
            # 注册功能
            user_form = RegisterUserForm(request.POST)
            if user_form.is_valid():
                user_form.save()

                response = HttpResponseRedirect('/')
                response.set_cookie('user_name', user_form.user_name, 3600)
                return response
            else:
                context['register_error_msg'] = '用户名/邮箱已注册'
                return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def user(request, user_name=''):

    # 获取当前登陆的用户
    current_user = get_current_user(request)
    if not current_user or (not user_name):
        return HttpResponseRedirect('/login/')



    # 如果是当前登陆的用户在查看自身的状态
    if current_user == user_name:
        user = User.objects.get(user_name=current_user)
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
        return render(request,
                      'user_profile.html',
                      {'current_user': user})
    else:
        try:
            user = User.objects.get(user_name=user_name)
        except:
            return HttpResponseNotFound('404 Not Found.')

        return render(request,
                      'people/other.html',
                      {'user': user})

# 注意，一个用户是不能看其他用户的购物车的。
# 所以，不需要在购物车之前指明用户
# 而是应该根据session和cookie判断当前登陆的用户
# 订单等等同理
def orders(request, order_status=None):
    current_user = get_current_user(request)
    try:
        current_user_obj = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        return render(request, 'error.html', {'error': e})
    order_list = Order.objects.filter(user=current_user_obj).order_by('start_time')
    if order_status:
        order_list = order_list.filter(status=order_status.uppper())

    context = {'orders': order_list,
               'order_status': order_status}

    return render(request, 'order/order.html', context)



def cart(request):
    current_user = get_current_user(request)
    if not current_user:
        return HttpResponseRedirect('/login/')

    user_obj = User.objects.get(user_name=current_user)
    user_s_cart = Cart.objects.filter(user=user_obj).order_
    context = {'cart': user_s_cart}

    return render(request, 'people/cart.html', context)

def market(request):
    # 展示加上超链接就足够
    current_user = get_current_user(request)
    categories = Category.objects.all()
    # to fill
    context = {'current_user': current_user,
                     'categories': categories}
    return render(request, 'index.html',context)

def cate_market(request, category_name):
    current_user = get_current_user(request)
    category_obj = Category.objects.get(pk=category_name)
    context = {'current_user': current_user,
               'category': category_obj}
    return render(request, 'market/category.html', context)

def goods_upload(request):
    current_user = get_current_user(request)
    if current_user == '':
        return HttpResponseRedirect('/login/')

    if request.method == 'POST':
        upload_goods = UploadGoodsForm(request.POST, request.FILES)
        if upload_goods.is_valid():
            new_goods = upload_goods.save(commit=False)
            new_goods.vendor = User.objects.get(user_name=current_user)
            if new_goods.start_bid and not new_goods.buy_it_now_price:
                new_goods.current_bid = new_goods.start_bid
                new_goods.sale_type = 'OA'
            elif new_goods.start_bid and new_goods.buy_it_now_price:
                new_goods.current_bid = new_goods.start_bid
                new_goods.sale_type = 'PB'
            elif not new_goods.start_bid and new_goods.buy_it_now_price:
                new_goods.sale_type = 'OB'
            else:
                return render(request, 'goods/upload.html',
                                          {'gf': upload_goods,
                                           'err_msg': '商品没有价格！'})

            new_goods.save()
            context = {}
            return render(request,'goods/uploadsuccess.html', context)
        return render(request,
                      'goods/upload.html',
                      {'gf': upload_goods,
                       'err_msg': '商品信息有误！'})
    else:
        upload_goods = UploadGoodsForm()
        return render(request,
                      'goods/upload.html',
                      {'gf': upload_goods})

def goods(request, goods_id, action=None):
    try:
        current_user = get_current_user(request)
    except ObjectDoesNotExist as e:
        current_user = None
    try:
        items = Goods.objects.get(pk=goods_id)
    except ObjectDoesNotExist as e:
        return render(request, 'error.html', {'error': e})
    context = {'goods': items}
    if action == None:
        return render(request, 'goods.html', context)
    elif action == 'addcart':
        addcart(request, current_user, goods_id)
    elif action == 'buynow':
        buynow(request, current_user, goods_id)
    elif action == 'auction':
        auction(request, current_user, goods_id)


def addcart(request, goods_id):
    current_user = get_current_user(request)
    #current_user转化成User对象
    user_obj = User.objects.get(user_name=current_user)
    if request.method == 'POST':
        # 要求加入购物车的POST要有这个表单
        item_count = request.POST['item_count']
        item_obj = Goods.objects.get(pk=goods_id)
        remaining = item_obj.remaining_number
        if remaining < item_count:
            # TO DO add an exception handler
            pass
        else:
            try:
                cart_item_obj = Cart.objects.get(user=user_obj, goods=item_obj)
                cart_item_obj.number += item_count
                cart_item_obj.save()
            except ObjectDoesNotExist as e:
                cart_item_obj = Cart(user=user_obj, goods=item_count, number=item_count)
                cart_item_obj.save()
        context = {'user': current_user,
                   'goods': item_obj,
                   'item_count': item_count}
        return render(request, 'addcart_success.html', context)
    return render(request, 'nothing_to_add.html')


# 实际上就是加入订单
def buynow(request, goods_id):
    current_user = get_current_user(request)

    user_obj = User.objects.get(user_name=current_user)
    item_obj = User.objects.get(goods_id=goods_id)
    if request.method == 'POST':
        item_count = request.POST['item_count']
        # 在前面做好物品数量要大于剩余数量的校验，在这里就不做校验了
        new_order = Order(user=user_obj, goods=item_obj, number=item_count)
        new_order.save()
        item_obj.remaining_number -= item_count
        item_obj.save()
        # 加入订单后转入到所有订单页面
        # 可以试试用session传递参数
        HttpResponseRedirect('/orders/unpaid')

def auction(request, goods_id):
    current_user = get_current_user(request)

    user_obj = User.objects.get(user_name=current_user)
    item_obj = User.objects.get(goods_id=goods_id)
    if request.method == 'POST':
        bid = request.POST['bid']
        current_bid = item_obj.current_bid
        if bid <= current_bid:
            return HttpResponseRedirect('/goods/%s' % goods_id)
        else:
            item_obj.current_bid = bid
            item_obj.current_bid_buyer = user_obj
            item_obj.save()
            # 如果没有买家出价的记录，就新建，否则就更新。
            try:
                auction_record = AuctionBid.objects.get(goods=item_obj, user=user_obj)
                auction_record.user_bid = bid
            except ObjectDoesNotExist as e:
                auction_record = AuctionBid(goods=item_obj, user=user_obj, user_bid=bid)
            auction_record.save()

# 查看一个用户的拍卖纪录
def bids(request):
    current_user = get_current_user(request)
    if not current_user:
        HttpResponseRedirect('/login/')
    user_obj = User.objects.get(user_name=current_user)
    auction_list = AuctionBid.objects.filter(user=user_obj)
    context = {'auction_list': auction_list}

    return render(request, 'people/auction_record.html', context)

def address(request):
    current_user = get_current_user(request)
    if not current_user:
        HttpResponseRedirect('/login/')
    user_obj = User.objects.get(user_name=current_user)
    address_list = DeliveryAddress.objects.filter(user=user_obj)

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address_form.user = user_obj
            address_form.save()
            return HttpResponseRedirect('/people/address')
        else:
            return HttpResponseRedirect('/people/address')

    context = {'address_list': address_list,
               'current_user': current_user}
    return render(request, 'people/address.html', context)

def new_address(request):
    pass
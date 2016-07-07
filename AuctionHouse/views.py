# -*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import *
from django.core.exceptions import *
from django.db.models import Q
from .models import *
from .forms import *
from .utils import *
from hashlib import md5
from PIL import Image
import os
from Crypto.PublicKey import RSA
# Create your views here.

def pay(request):
    pass

def index(request):
    #user_name = get_current_user(request)
    # categories = Category.objects.all()
    # return render(request, 'index.html', {'user_name':user_name})
    return market(request)


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
                m2 = md5()
                m2.update(password.encode('utf8'))
                password = m2.hexdigest()

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
                new_user = user_form.save(commit=False)
                m2 = md5()
                m2.update(new_user.password.encode('utf8'))
                new_user.password = m2.hexdigest()
                # 对用户信息用服务器的公钥加密
                pub_key = RSA.importKey(open(r"D:\id_rsa.pub").read())
                new_user.phone = pub_key.encrypt(new_user.phone.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))
                new_user.phone = new_user.phone.decode(encoding="utf-8")
                new_user.real_id = pub_key.encrypt(new_user.real_id.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))
                new_user.real_id = new_user.real_id.decode(encoding="utf-8")
                new_user.real_name = pub_key.encrypt(new_user.real_name.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))
                new_user.real_name = new_user.real_name.decode(encoding="utf-8")
                # 存储在服务器中的是经过加密的用户信息
                new_user.save()

                response = HttpResponseRedirect('/')
                response.set_cookie('user_name', new_user.user_name, 3600)
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
                update_user = user_form.save(commit=False)
                pub_key = RSA.importKey(open(r"D:\id_rsa.pub").read())
                update_user.phone = update_user.encrypt(update_user.phone.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))
                update_user.phone = update_user.phone.decode(encoding="utf-8")
                update_user.real_id = pub_key.encrypt(update_user.real_id.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))
                update_user.real_id = update_user.real_id.decode(encoding="utf-8")
                update_user.real_name = pub_key.encrypt(update_user.real_name.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))
                update_user.real_name = update_user.real_name.decode(encoding="utf-8")

        pri_key = RSA.importKey(open(r"D:\id_rsa").read())
        user_phone = pri_key.decrypt(user.phone.encode(encoding="utf-8")).decode("utf-8")
        user_real_id = pri_key.decrypt(user.real_id.encode(encoding="utf-8")).decode("utf-8")
        user_real_name = pri_key.decrypt(user.phone.encode(encoding="utf-8")).decode("utf-8")
        user.phone = user_phone
        user.real_id = user_real_id
        user.real_name = user_real_name
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
        return HttpResponseRedirect('/login')

    order_list = Order.objects.filter(user=current_user_obj).order_by('start_time')
    if order_status:
        order_list = order_list.filter(status=order_status.upper())

    context = {'orders': order_list,
               'order_status': order_status,
               'current_user': current_user_obj}

    return render(request, 'orders.html', context)

def cart(request):
    current_user = get_current_user(request)
    try:
        user_obj = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        return HttpResponseRedirect('/login')
    user_s_cart = Cart.objects.filter(user=user_obj)
    context = {'cart': user_s_cart,
               'current_user': user_obj}

    return render(request, 'cart.html', context)

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
    categories = Category.objects.all()
    category_obj = categories.get(pk=category_name)
    context = {'current_user': current_user,
               'categories': categories,
               'category': category_obj}
    return render(request, 'category_market.html', context)

def goods_upload(request):
    current_user = get_current_user(request)
    if current_user == '':
        return HttpResponseRedirect('/login/')
    user_obj = User.objects.get(user_name=current_user)
    categories = Category.objects.all()
    context = {'current_user': user_obj, 'categories': categories}
    if request.method == 'POST':
        upload_goods = UploadGoodsForm(request.POST, request.FILES)
        context['gf'] = upload_goods
        if upload_goods.is_valid():

            new_goods = upload_goods.save(commit=False)
            # 创建缩略图
            # shop 268*249
            # detail 329*380
            # cart 110*110
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            raw_image = request.FILES['image_description']
            img = Image.open(raw_image)
            #img.crop((0, 0, 268, 249))
            img.resize((268, 249))
            url1='goods_image/' + '1_' + raw_image.name
            img.save(os.path.join(MEDIA_ROOT,url1), 'jpeg')
            img2 = Image.open(raw_image)
            #img2.crop((0, 0, 329,  380))
            img2.resize((329, 380))
            url2='goods_image/' + '2_' + raw_image.name
            img2.save(os.path.join(MEDIA_ROOT,url2), 'jpeg')
            img3 = Image.open(raw_image)
            img3.thumbnail((110, 110), Image.ANTIALIAS)
            url3='goods_image/' + '3_' + raw_image.name
            img3.save(os.path.join(MEDIA_ROOT,url3), 'jpeg')
            new_goods.image_description_2 = url1
            new_goods.image_description_3 = url2
            new_goods.image_description_4 = url3
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
                context['err_msg'] = '商品没有价格！'
                return render(request, 'upload_item.html', context)

            new_goods.save()
            return HttpResponseRedirect('/')
        context['err_msg'] = '商品信息有误！'
        return render(request,
                      'upload_item.html', context)
    else:
        upload_goods = UploadGoodsForm()
        context['gf'] = upload_goods
        return render(request,
                      'upload_item.html', context)

def goods(request, goods_id, action=None):
    categories = Category.objects.all()
    current_user = get_current_user(request)
    try:
        user_obj = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        user_obj = None
    try:
        item = Goods.objects.get(pk=goods_id)
    except ObjectDoesNotExist as e:
        return render(request, 'error.html', {'error': e})

    context = {'goods': item,
               'current_user': user_obj,
               'categories': categories}

    if request.method == 'POST':
        if 'addcart' in request.POST:
            addcart_form = AddCartForm(request.POST)
            if addcart_form.is_valid():
                item_count = addcart_form.cleaned_data['item_count']
                remaining = item.remaining_number
                if remaining < item_count:
                    return HttpResponseBadRequest()
                    # TO DO add an exception handler
                    pass
                else:
                    try:
                        cart_item_obj = Cart.objects.get(user=user_obj, goods=item)
                        cart_item_obj.number += item_count
                        cart_item_obj.save()
                    except ObjectDoesNotExist as e:
                        cart_item_obj = Cart(user=user_obj, goods=item, number=item_count)
                        cart_item_obj.save()
                context = {'current_user': current_user,
                           'goods': item,
                           'categories': categories,
                           'item_count': item_count}
                return HttpResponseRedirect('/cart')
            else:
                return HttpResponseBadRequest()
        elif 'buy_now' in request.POST:
            buynow_form = AddCartForm(request.POST)
            if buynow_form.is_valid():
                item_count = buynow_form.cleaned_data['item_count']
                if item.remaining_number < item_count:
                    return HttpResponseBadRequest()
                else:
                    new_order = Order(user=user_obj, goods=item, number=item_count)
                    new_order.save()
                    item.remaining_number -= item_count
                    item.save()
                    return HttpResponseRedirect('/orders/unpaid')
            else:
                return HttpResponseBadRequest()
        elif 'auction_bid' in request.POST:
            auction_bid_form = AuctionBidForm(request.POST)
            if auction_bid_form.is_valid():
                bid = auction_bid_form.cleaned_data['bid']
                current_bid = item.current_bid
                if bid <= current_bid:
                    return HttpResponseRedirect('/goods/%s' % goods_id)
                else:
                    item.current_bid = bid
                    item.current_bid_buyer = user_obj
                    item.save()
                    # 如果没有买家出价的记录，就新建，否则就更新。
                    try:
                        auction_record = AuctionBid.objects.get(goods=item, user=user_obj)
                        auction_record.user_bid = bid
                    except ObjectDoesNotExist as e:
                        auction_record = AuctionBid(goods=item, user=user_obj, user_bid=bid)
                    auction_record.save()
    return render(request, 'product-details.html', context)

    # if action == None:
    #     return render(request, 'product-details.html', context)
    # elif action == 'addcart':
    #     addcart(request, current_user, goods_id)
    # elif action == 'buynow':
    #     buynow(request, current_user, goods_id)
    # elif action == 'auction':
    #     auction(request, current_user, goods_id)

def addcart(request, goods_id):
    current_user = get_current_user(request)
    #current_user转化成User对象
    user_obj = User.objects.get(user_name=current_user)
    if request.method == 'POST':
        # 要求加入购物车的POST要有这个表单
        if 'item_count' in request.POST:

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
    try:
        user = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        return HttpResponseRedirect('/login')
    auction_list = AuctionBid.objects.filter(user=user)
    context = {'auction_list': auction_list}

    return render(request, 'people/auction_record.html', context)

def new_address(request):
    current_user = get_current_user(request)
    try:
        user = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        return HttpResponseRedirect('/login')
    # 数据库中读出的用户信息解密
    pri_key = RSA.importKey(open(r"D:\id_rsa").read())
    user_phone = pri_key.decrypt(user.phone.encode(encoding="utf-8")).decode("utf-8")
    user_real_id = pri_key.decrypt(user.real_id.encode(encoding="utf-8")).decode("utf-8")
    user_real_name = pri_key.decrypt(user.phone.encode(encoding="utf-8")).decode("utf-8")
    user.phone = user_phone
    user.real_id = user_real_id
    user.real_name = user_real_name
    address_list = DeliveryAddress.objects.filter(user=user)
    context = {'current_user': user,
               'address_list': address_list}
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = DeliveryAddress(user=user, **address_form.cleaned_data)
            address.save()
        return render(request, 'user_profile.html', context)

    return render(request, 'newaddress.html', context)

def checkout(request, order_id):
    # 我实现不了支付系统。这里的checkout实际上是为订单填上收货地址将订单补充完整
    current_user = get_current_user(request)
    try:
        user = User.objects.get(user_name=current_user)
    except ObjectDoesNotExist as e:
        return HttpResponseRedirect('/login')
    order = Order.objects.get(pk=order_id)
    address_list = DeliveryAddress.objects.filter(user=user)
    context = {'address_list': address_list,
               'order': order,
               'current_user': current_user}

    if request.method == 'POST':
        address_form = AddressChooseForm(request.POST, instance=order)
        if address_form.is_valid():
            order.address = address_form.address
            order.status = 'UNCONFIRMED'
            order.save()

            return HttpResponseRedirect('/')

    return render(request, 'checkout.html', context)
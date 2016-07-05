# -*-coding:utf-8-*-
from django.db import models

# Create your models here.

class User(models.Model):
    # user_id = models.CharField(max_length=36, primary_key=True)
    user_name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    real_name = models.CharField(max_length=30)
    real_id = models.CharField(max_length=30)

    # 性别，默认为男
    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=20, choices=GENDER, default=MALE)
    portrait = models.ImageField(upload_to='user_portrait/')
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=30)
    # 信用等级
    credit = models.FloatField(default=0)

class DeliveryAddress(models.Model):
    # address_id = models.CharField(max_length=36, primary_key=True)
    user_id = models.ForeignKey(User)
    delivery_phone = models.CharField(max_length=30)
    delivery_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=30)


class Goods(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor')
    remaining_number = models.PositiveIntegerField()
    goods_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)

    ON_SALE = 'ON'
    OFF_SHELVES = 'OFF'
    STATUS = (
        (ON_SALE, 'ON SALE'),
        (OFF_SHELVES, 'OFF SHELVES'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default=ON_SALE)

    ONLY_AUCTION = 'OA'
    PLUS_BUYITNOW = 'PB'
    ONLY_BUYITNOW = 'OB'
    SALE_TYPE = (
        (ONLY_AUCTION, '仅限拍卖'),
        (ONLY_BUYITNOW, '拍卖与一口价'),
        (PLUS_BUYITNOW, '仅限一口价'),
    )
    sale_type = models.CharField(max_length=30, choices=SALE_TYPE, blank=True, null=True)
    start_bid = models.SmallIntegerField(blank=True, null=True)
    current_bid = models.SmallIntegerField(blank=True, null=True)
    current_bid_buyer = models.ForeignKey(User, blank=True, null=True, related_name='current_bid_buyer')
    buy_it_now_price = models.SmallIntegerField(blank=True, null=True)
    # 商品可以有起拍价和一口价，可以只有两个中的一个，但至少要有一个。
    # 根据商品的各自价格，将商品分为仅拍卖、拍卖或一口价、仅一口价三种。
    # 但是，数量为多个的商品是不能拍卖的。（除非成组拍卖，但是成组拍卖的时候算作一个商品）

    image_description = models.ImageField(upload_to='goods_image/%Y/%m/%d', blank=True, null=True)
    image_description_2 = models.ImageField(upload_to='goods_image/%Y/%m/%d', blank=True, null=True)
    image_description_3 = models.ImageField(upload_to='goods_image/%Y/%m/%d', blank=True, null=True)
    image_description_4 = models.ImageField(upload_to='goods_image/%Y/%m/%d', blank=True, null=True)
    image_description_5 = models.ImageField(upload_to='goods_image/%Y/%m/%d', blank=True, null=True)


class AuctionBid(models.Model):
    goods = models.ForeignKey(Goods)
    user = models.ForeignKey(User)
    user_bid = models.SmallIntegerField()
    bid_time = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    goods = models.ForeignKey(Goods)
    number = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User)


class Order(models.Model):
    goods = models.ForeignKey(Goods)
    user = models.ForeignKey(User)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    DONE = 'DONE'
    DOING = 'DOING'
    ABORTED = "AB"
    ORDER_STATUS = (
        (DONE, '交易完成'),
        (DOING, '正在进行'),
        (ABORTED, '交易关闭'),
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=DOING)


# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-03 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_bid', models.SmallIntegerField()),
                ('bid_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_phone', models.CharField(max_length=30)),
                ('delivery_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_number', models.PositiveIntegerField()),
                ('goods_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('ON', 'ON SALE'), ('OFF', 'OFF SHELVES')], default='ON', max_length=20)),
                ('sale_type', models.CharField(blank=True, choices=[('OA', '仅限拍卖'), ('OB', '拍卖与一口价'), ('PB', '仅限一口价')], max_length=30)),
                ('start_bid', models.SmallIntegerField(blank=True)),
                ('current_bid', models.SmallIntegerField(blank=True)),
                ('buy_it_now_price', models.SmallIntegerField(blank=True)),
                ('image_description', models.ImageField(blank=True, upload_to='goods_image/%Y/%m/%d')),
                ('image_description_2', models.ImageField(blank=True, upload_to='goods_image/%Y/%m/%d')),
                ('image_description_3', models.ImageField(blank=True, upload_to='goods_image/%Y/%m/%d')),
                ('image_description_4', models.ImageField(blank=True, upload_to='goods_image/%Y/%m/%d')),
                ('image_description_5', models.ImageField(blank=True, upload_to='goods_image/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True)),
                ('status', models.CharField(choices=[('DONE', '交易完成'), ('DOING', '正在进行'), ('AB', '交易关闭')], default='DOING', max_length=20)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('real_name', models.CharField(max_length=30)),
                ('real_id', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=20)),
                ('portrait', models.ImageField(blank=True, upload_to='user_portrait/')),
                ('birthday', models.DateField(blank=True)),
                ('phone', models.CharField(max_length=30)),
                ('credit', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.User'),
        ),
        migrations.AddField(
            model_name='goods',
            name='current_bid_buyer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_bid_buyer', to='AuctionHouse.User'),
        ),
        migrations.AddField(
            model_name='goods',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='AuctionHouse.User'),
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.User'),
        ),
        migrations.AddField(
            model_name='cart',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.Goods'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.User'),
        ),
        migrations.AddField(
            model_name='auctionbid',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.Goods'),
        ),
        migrations.AddField(
            model_name='auctionbid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuctionHouse.User'),
        ),
    ]

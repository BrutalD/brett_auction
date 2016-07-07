# -*-coding:utf-8-*-

from django.conf.urls import url
from . import views
from django.contrib import admin
import os
from brett_auction import settings


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^login/$', views.login_register, name='login'),
#    url(r'^register/$', views.register, name='register'),
    url(r'^people/$', views.user, name='user'),
    url(r'^people/(?P<user_name>.+)/$', views.user,name='user'),
    url(r'^bids/$',views.bids, name='user_bids'),
    url(r'^orders/$',views.orders, name='user_orders'),
    url(r'^orders/(?P<order_status>[a-z]+)/$', views.orders, name='orders_with_status'),
    url(r'^goods/(?P<goods_id>[0-9])/(?P<action>[a-z])/', views.goods, name='goods_action'),
    url(r'^goods/(?P<goods_id>[0-9])/', views.goods, name='goods_detail'),
    url(r'^newaddress/', views.new_address, name='new_address'),
    # url(r'^orders/unsent/$', views.orders_unsent, name='orders_unsent'),
    # url(r'^orders/unconfirmed/$', views.orders_unconfirmed, name='orders_unconfirmed'),
    url(r'^/$', views.index, name='index'),
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(?P<category_name>.+)/$', views.cate_market, name='market_of_a_category'),
    url(r'^upload/$', views.goods_upload, name='goods_upload'),
    url(r'^checkout/(?P<order_id>[0-9]+)/$', views.checkout, name='checkout'),
    url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^css/(?P<path>.*)', 'django.views.static.serve',{'document_root':os.path.join(settings.BASE_DIR, 'AuctionHouse/templates/css/')}),
    url(r'^images/(?P<path>.*)', 'django.views.static.serve',{'document_root':os.path.join(settings.BASE_DIR, 'AuctionHouse/templates/images/')}),
    url(r'^js/(?P<path>.*)', 'django.views.static.serve',{'document_root':os.path.join(settings.BASE_DIR, 'AuctionHouse/templates/js/')}),
    url(r'^fonts/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(settings.BASE_DIR, 'AuctionHouse/templates/fonts/')}),
]
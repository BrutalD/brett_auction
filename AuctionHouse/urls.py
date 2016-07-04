# -*-coding:utf-8-*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^people/(?P<user_name>[a-zA-Z0-9_]+)/$', views.user,name='user'),
    url(r'^bids/$',views.bids, name='user_bids'),
    url(r'^orders/$',views.orders, name='user_orders'),
    url(r'^orders/unpaid/$', views.orders_unpaid, name='orders_unpaid'),
    url(r'^orders/unsent/$', views.orders_unsent, name='orders_unsent'),
    url(r'^orders/unconfirmed/$', views.orders_unconfirmed, name='orders_unconfirmed'),
    url(r'^market/$', views.market, name='market')
]
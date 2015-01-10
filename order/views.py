# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response

from order.models import Order, OrderItem
from order.forms import OrderForm
from product.models import Product
from product.models import Category

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.template import RequestContext

import json
import datetime

def get_category():
    categorys = Category.objects.all()
    return categorys

def order_view(request, templateName):
    # if 'openid' not in request.session:
    #     return HttpResponseRedirect('/')
    openid = '123456789'
    orders = Order.objects.filter(openid = openid, isPaid = False, isCancel = False).order_by('-datetime')
    for order in orders:
        order.items = OrderItem.objects.filter(order = order)
    return render_to_response(templateName, {
        'orders' : orders,
        'categorys' : get_category(),
        }, context_instance = RequestContext(request))

def havepay_view(request, templateName):
    # if 'openid' not in request.session:
    #     return HttpResponseRedirect('/')
    openid = '123456789'
    orders = Order.objects.filter(openid = openid, isPaid = True, isCancel = False).order_by('-datetime')
    for order in orders:
        order.items = OrderItem.objects.filter(order = order)
    return render_to_response(templateName, {
        'orders' : orders,
        'categorys' : get_category(),
        })

def havecancel_view(request, templateName):
    # if 'openid' not in request.session:
    #     return HttpResponseRedirect('/')
    openid = '123456789'
    orders = Order.objects.filter(openid = openid, isPaid =False, isCancel = True).order_by('-datetime')
    for order in orders:
        order.items = OrderItem.objects.filter(order = order)
    return render_to_response(templateName, {
        'orders' : orders,
        'categorys' : get_category(),
        })

def create_order(request):
    # if 'openid' not in request.session:
    #     return HttpResponseRedirect('/')
    request.session['openid'] = '123456789'
    #print request.method
    if request.method == 'POST':
        print "haha create_order+++   1"
        #form = OrderForm(request.POST)
        openid = request.session['openid']
        order_id = 0
        for char in openid:
            order_id += ord(char)
        #cart = request.session['cart']
        uid = request.POST.get('uid')
        number = request.POST.get('number')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        addr = request.POST.get('address')
        price = request.POST.get('price')
        send = request.POST.get('send')
        print "create_order+++  2", order_id
        print uid, number, name, phone, addr, price, send
        # if form.is_valid():
        # clean = form.cleaned_data

        order = Order.objects.create(
            id = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(order_id)),
            openid = request.session['openid'],
            name = name,
            phone = phone,
            address = addr,
            price = price,
            )
        # for key, value in cart.items.items():
        key = uid
        product = Product.objects.get(uid = key)
        OrderItem.objects.create(
            order = order,
            product = product,
            number = number,
            )
        # cart.clear()
        # request.session['cart'] = cart
        request.session['orderid'] =  order_id
        return HttpResponseRedirect('/order/')
    else:
        form = OrderForm()
    print "why not+++++++++++++++++"
    return HttpResponseRedirect('/order/')

@csrf_exempt
def cancel_order(request):
    success = False
    message = ''
    if request.method == 'POST':
        orderID = request.POST.get('orderID', None)
        if orderID:
            order = Order.objects.get(id = orderID)
            if order.isDelivery is False:
                order.isCancel = True
                success = True
                order.save()
            else:
                message = '卖家已经发货'
        else:
            message = '此订单不存在'
    return HttpResponse(json.dumps({
        'success' : success,
        'message' : message,
        }))

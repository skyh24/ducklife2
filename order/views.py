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
    if request.method == 'POST':
        form = OrderForm(request.POST)
        openid = request.session['openid']
        order_id = 0
        for char in openid:
            order_id += ord(char)
        cart = request.session['cart']
        print "create_order+++", cart
        if form.is_valid() and cart.empty() is not True:
            clean = form.cleaned_data
            order = Order.objects.create(
                id = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(order_id)),
                openid = request.session['openid'],
                name = clean['name'],
                phone = clean['phone'],
                address = clean['address'],
                price = cart.total,
                )
            for key, value in cart.items.items():
                product = Product.objects.get(uid = key)
                OrderItem.objects.create(
                    order = order,
                    product = product,
                    number = value,
                    )
            cart.clear()
            request.session['cart'] = cart
            return HttpResponseRedirect('/order/')
    else:
        form = OrderForm()
    return render_to_response(templateName, {
        'form' : form,
        'categorys' : get_category(),
        })

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

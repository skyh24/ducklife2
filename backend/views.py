# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from order.models import Order, OrderItem
from product.models import Product, Category
from product.forms import ProductForm

from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from lxml import etree

import json
import datetime
import settings
import os.path

def backend_view(request, templateName):
    notOrders = Order.objects.filter(isPaid = False,
        isCancel = False, isDelivery = False).order_by('-datetime')
    for order in notOrders:
        order.items = OrderItem.objects.filter(order = order)
    waitingOrders = Order.objects.filter(isDelivery = False,
        isCancel = False, isPaid = True).order_by('-datetime')
    for order in waitingOrders:
        order.items = OrderItem.objects.filter(order = order)
    completeOrders = Order.objects.filter(isDelivery = True,
        isCancel = False, isPaid = True).order_by('-datetime')
    for order in completeOrders:
        order.items = OrderItem.objects.filter(order = order)
    cancelOrders = Order.objects.filter(isCancel = True).order_by('-datetime')
    for order in cancelOrders:
        order.items = OrderItem.objects.filter(order = order)
    products = Product.objects.all().order_by('-datetime')
    categorys = Category.objects.all().order_by('-datetime')
    for item in categorys:
        item.products = Product.objects.filter(category = item)
    return render_to_response(templateName, {
        'notOrders' : notOrders,
        'waitingOrders' : waitingOrders,
        'completeOrders' : completeOrders,
        'cancelOrders' : cancelOrders,
        'products' : products,
        'categorys' : categorys,
        }, context_instance = RequestContext(request))

@csrf_exempt
def create_category(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name:
            category = Category.objects.create(
                name = name
                )
            category.products = None
            success = True
            return render_to_response('category.html', {
                'category' : category
                })
    raise Http404()

@csrf_exempt
def create_product(request):
    success = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            clean = form.cleaned_data
            ###########################
            html = clean['description']
            page = etree.HTML(html.lower().decode('utf-8'))
            ps = page.xpath(u"//p")
            desc = ''.join(ps)
            print "create_product+++", desc
            try:
                category = Category.objects.get(id = clean['category'])
            except:
                raise Http404()
            product = Product.objects.create(
                uid = datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                name = clean['name'],
                # description = clean['description'],
                description = desc,
                price = clean['price'],
                picture = clean['picture'],
                category = category,
                )
            success = True
        return HttpResponseRedirect('/backend/')
    else:
        raise Http404()

def delete_product(request):
    success = False
    if request.method == 'GET':
        productId = request.GET.get('uid', None)
        if productId:
            product = Product.objects.get(uid = productId)
            product.delete()
            success = True
        return HttpResponse(json.dumps({
            'success' : success,
            }))
    else:
        raise Http404()

def delete_category(request):
    success = False
    if request.method == 'GET':
        categoryId = request.GET.get('categoryId', None)
        if categoryId:
            category = Category.objects.get(id = categoryId)
            category.delete()
            success = True
        return HttpResponse(json.dumps({
            'id' : categoryId,
            'success' : success,
            }))
    raise Http404()

def delivery_order(request):
    success = False
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if id:
            order = Order.objects.get(id = id)
            order.isDelivery = True
            order.save()
            success = True
    return HttpResponse(json.dumps({
        'success' :success,
        }))

def cancel_order(request):
    success = False
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if id:
            order = Order.objects.get(id = id)
            order.isCancel = True
            order.save()
            success = True
    return HttpResponse(json.dumps({
        'success' :success,
        }))

def paid_order(request):
    success = False
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if id:
            order = Order.objects.get(id = id)
            order.isPaid = True
            order.isDelivery = True         #####################
            order.save()
            success = True
    return HttpResponse(json.dumps({
        'success' :success,
        }))

def upload_pictures(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pictures')
        path = os.path.join(settings.PROJECT_PATH, 'media/pictures/').replace('\\', '/')
        result = ''
        for file in files:
            time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = time + file.name
            destination = open(path + filename, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            result += '/media/pictures/' + filename + '\n'
        return HttpResponse(result)
    return HttpResponse('上传失败')
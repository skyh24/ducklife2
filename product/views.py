# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str, smart_unicode 
from product.models import Product, Category, Cart, Customer

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET 

from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

import json

def index_view(request, templateName):
    if 'openid' not in request.session:
        return HttpResponseRedirect('/code/?next=/')
    products = Product.objects.all()[:5]
    categorys = Category.objects.all()
    return render_to_response(templateName, {
        'products' : products,
        'categorys' : categorys,
        })

def kefu_view(request):
    
    reply_xml = """<xml>
       <ToUserName><![CDATA[%s]]></ToUserName>
       <FromUserName><![CDATA[%s]]></FromUserName>
       <CreateTime>%s</CreateTime>
       <MsgType><![CDATA[text]]></MsgType>
       <Content><![CDATA[%s]]></Content>
       </xml>"""%(FromUserName,ToUserName,CreateTime,"小主有任何疑问都可以拨打服务热线，客服小鲜将真诚耐心的为您服务。服务热线: 4000020864")

    return HttpResponse(reply_xml)
    #return render_to_response(templateName, {})

def product_view(request, c_id, templateName):
    # if 'openid' not in request.session:
    #     return HttpResponseRedirect('/code/?next=/' + c_id + '/product/')
    category = Category.objects.get(id = c_id)
    categoryName = category.name
    products = Product.objects.filter(category = category)
    categorys = Category.objects.all()
    return render_to_response(templateName, {
         'products' : products,
         'categorys' : categorys,
         'categoryName' : categoryName,
        })

def product_detail_view(request, p_id, templateName):
    # if 'openid' not in request.session:
    #    return HttpResponseRedirect('/code/?next=/product/' + p_id + '/')
    ####你要加默认地址2个的
    request.session['openid'] = '1234567'  #debug
    openid = request.session['openid']
    print "openid+++", openid
    try:
        customer = Customer.objects.get(openid = openid)
    except:
        print "new customer+++++"
        customer = Customer.objects.create(
            openid = openid,
            addrone = "点击添加上面默认地址",
            addrtwo = "点击添加上面默认地址",
            )
    print "customer+++", customer
    product = Product.objects.get(uid = p_id)
    categorys = Category.objects.all()
    return render_to_response(templateName, {
        'customer' : customer,
        'product' : product,
        'categorys' : categorys,
        }, context_instance = RequestContext(request))

@csrf_exempt
def add_address(request):
    success = False
    if request.method == 'POST':
        openid = request.session['openid']
        addrone = request.POST.get('addr1', None)
        addrtwo = request.POST.get('addr2', None)
        customer = Customer.objects.get(openid = openid)
        customer.addrone = addrone
        customer.addrtwo = addrtwo
        customer.save()
    return HttpResponse(json.dumps({
        'success' : success,
        }))

def cart_view(request, templateName):
    # if 'openid' not in request.session:
    #     return HttpResponseRedirect('/code/?next=/cart/')
    cart = get_cart(request)
    print "cart_view+++", cart
    products = []
    for key, value in cart.items.items():
        item = Product.objects.get(uid = key)
        item.number = value
        products.append(item)
    categorys = Category.objects.all()
    return render_to_response(templateName, {
        'products' : products,
        'price' : cart.total,
        'categorys' : categorys,
        }, context_instance = RequestContext(request))

def get_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = Cart()
    return request.session['cart']

def clear_cart(request):
    success = False
    if request.method == 'POST':
        if 'cart' in request.session:
            request.session['cart'].clear()
        cart = get_cart(request)
        success = True
    return HttpResponse(json.dumps({
        'success' : success,
        }))

@csrf_exempt
def add_product(request):
    success = False
    if request.method == 'POST':
        productID = request.POST.get('productID', None)
        number = request.POST.get('number', None)
        del request.session['cart']
        cart = get_cart(request)
        print "add_product+++", cart ###
        if productID:
            product = Product.objects.get(uid = productID)
            cart.add(product,number)
            request.session['cart'] = cart
            print "yes+++",  request.session['cart'] ###
            success = True
    return HttpResponse(json.dumps({
        'success' : success,
        }))

def reduce_product(request):
    success = False
    if request.method == 'POST':
        productID = request.POST.get('productID', None)
        cart = get_cart(request)
        if productID:
            product = Product.objects.get(uid = productID)
            cart.reduce(product)
            success = True
    return HttpResponse(json.dumps({
        'success' : success,
        }))

@csrf_exempt
def cancel_product(request):
    success = False
    if request.method == 'POST':
        productID = request.POST.get('productID', None)
        number = request.POST.get('number', None)
        cart = get_cart(request)
        if productID:
            product = Product.objects.get(uid = productID)
            cart.cancel(product,number)
            request.session['cart'] = cart
            success = True
    return HttpResponse(json.dumps({
        'success' : success,
        'total':request.session['cart'].total
        }))

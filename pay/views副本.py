# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response

from order.models import Order
from order.forms import OrderForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.template import RequestContext

import json
import datetime

@csrf_protect
def payConfirm_view(request, templateName):
    if 'openid' not in request.session:
        return HttpResponseRedirect('/')

    openid = request.session['openid']

    if request.method == "POST":
        orderid = request.POST.get('orderid')
        order = Order.objects.get(id=orderid)
        totalPrice = order.price
        if order.openid != openid:
            raise Http404()

    return render_to_response(templateName,
        {'totalPrice' : totalPrice,
         'orderid' : orderid,
        })

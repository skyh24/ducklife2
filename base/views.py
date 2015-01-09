# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.http import HttpResponse, HttpResponseRedirect
from weixin import *

import settings

def get_code(request):
    next = request.GET.get('next', '/')
    if 'openid' in request.session:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(
    #     'https://open.weixin.qq.com/connect/oauth2/authorize?scope=snsapi_base&state=dengyh&redirect_uri=http%3A%2F%2F59.56.65.211%2Fopenid%2F%3Fnext%3D%2F&response_type=code&appid=wxda5a961b55b6f822#wechat_redirect')
        getCode(settings.APPID, 'http://59.56.65.211/openid/?next=' + next))

def get_openid(request):
    code = request.GET.get('code', None)
    next = request.GET.get('next', None)
    if 'openid' in request.session:
        return HttpResponseRedirect(next)
    if code and next:
        openid = getOpenid(settings.APPID,
            settings.APPSECRET, code)
        request.session['openid'] = openid
    return HttpResponseRedirect(next)

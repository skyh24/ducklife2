# -*- coding: utf-8 -*-
import urllib, urllib2
import hashlib, json
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode 
import xml.etree.ElementTree as ET 
from django.views.decorators.csrf import csrf_exempt 

TOKEN = "xiaoxian"

@csrf_exempt
def accessInterface(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response
    if request.method == 'POST':
        print "post+++"
        response = HttpResponse(responseMsg(request))
        return response
    else:
        return "can not access"

def checkSignature(request):
    global TOKEN
    echostr = request.GET.get('echostr', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    signature = request.GET.get('signature', None)
    token = TOKEN

    tmpList = [token,timestamp,nonce]  
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList) 
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:  
        return echoStr  
    else:  
        return "can not access wechat"  


def responseMsg(request):
    print request.body
    xmlstr = smart_str(request.body)
    xml = ET.fromstring(xmlstr)

    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime = xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text
    #Content = xml.find('Content').text
    #MsgId = xml.find('MsgId').text

    if MsgType == 'text':
        Content = '小主有任何疑问都可以拨打服务热线，客服小鲜将真诚耐心的为您服务。服务热线: 4000020864'
    else:
        MsgEvent = xml.find('Event').text
        if MsgEvent == 'subscribe':
            Content = '终于等到你了，小主，欢迎关注肉小鲜加入鲜客一族。试运营期间肉小鲜采用预购模式，小主可以选择周五，周六，周天任意一天由顺丰进行冷运宅配。全部食材都是在配送当天早上由宁夏盐池空运而来，在广州新鲜包装！为了让客户更加安心的体验肉小鲜产品，我们决定采用货到付款方式！小主满意后再收货。目前肉小鲜业务覆盖广州，深圳两地。'
        else:
            Content = "您好，您的反馈信息已收到，需要的话请留下联系电话，我们客服会进一步跟踪处理，我们的进步需要您的支持与鼓励^_^"
    print "msg+++", Content
    reply_xml = """<xml>
       <ToUserName><![CDATA[%s]]></ToUserName>
       <FromUserName><![CDATA[%s]]></FromUserName>
       <CreateTime>%s</CreateTime>
       <MsgType><![CDATA[text]]></MsgType>
       <Content><![CDATA[%s]]></Content>
       </xml>"""%(FromUserName,ToUserName,CreateTime,Content)

    return HttpResponse(reply_xml)


def getOpenid(appid, appsecret, code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + \
        appid + '&secret=' + \
        appsecret + '&code=' + \
        code + '&grant_type=authorization_code'
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    openid = data['openid']
    return openid

def getCode(appid, redirect_uri):
    response_type = 'code'
    scope = 'snsapi_userinfo'
    state = 'dengyh'
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?'
    queryString = urllib.urlencode({
        'appid' : appid,
        'redirect_uri' : redirect_uri,
        'response_type' : response_type,
        'scope' : scope,
        'state' : state,
        })
    print url + queryString +"#wechat_redirect"
    return url + queryString +"#wechat_redirect"

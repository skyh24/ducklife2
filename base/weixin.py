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
        Content = '您好，您的反馈信息已收到，需要的话请留下联系电话，我们客服会进一步跟踪处理，我们的进步需要您的支持与鼓励^_^'
    else:
        MsgEvent = xml.find('Event').text
        if MsgEvent == 'subscribe':
            Content = '终于等到你了，小主。欢迎关注肉小鲜加入鲜客一族，我们精选全球各地最优质新鲜的食材，全程冷藏配送，我们追求食材的极致新鲜和绝对安全！目前我们为小主推出第一款产品——宁夏盐池滩羊肉，滩羊在当地宰杀之后当天经由空运到达广州，最后由顺丰在小主下单的次日冷运宅配到家，整个过程保持在24小时之内，小主可放心食用。目前肉小鲜业务覆盖广州、深圳两地。'
        else:
            Content = "小主有任何疑问或者建议都可以回复小鲜客服或者直接拔打服务热线：4000020864，小鲜客服将真诚耐心的为你服务。谢谢小主的来访。"
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

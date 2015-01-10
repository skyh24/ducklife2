import urllib, urllib2
import hashlib, json
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode 
import xml.etree.ElementTree as ET  

TOKEN = "xiaoxian"

def accessInterface(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response
    if request.method == 'POST':
        response = HttpResponse(responseMsg(request),content_type="application/xml")
        return response
    else
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
    xmlstr = smart_str(request.body)
    xml = ET.fromstring(xmlstr)

    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime = xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text
    Content = xml.find('Content').text
    MsgId = xml.find('MsgId').text
    if Content == ''
        Content = 'welcome'
    reply_xml = """<xml>
       <ToUserName><![CDATA[%s]]></ToUserName>
       <FromUserName><![CDATA[%s]]></FromUserName>
       <CreateTime>%s</CreateTime>
       <MsgType><![CDATA[text]]></MsgType>
       <Content><![CDATA[%s]]></Content>
       </xml>"""%(FromUserName,ToUserName,CreateTime,Content + "  Hello world, this is test message")

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

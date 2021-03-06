import urllib, urllib2
import hashlib, json

def accessInterface(request):
    echostr = request.GET.get('echostr', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    signature = request.GET.get('signature', '')
    if checkSignature(signature, 'xiaoxian', timestamp, nonce):
        return HttpResponse(echostr)
    else:
        return HttpResponse('Can not access Weixin interface')

def checkSignature(signature, token, timestamp, nonce):
    tmpArr = [token, timestamp, nonce]
    tmpArr = sorted(tmpArr)
    tmpStr = ''.join(tmpArr)
    sha1Str = hashlib.sha1(tmpStr).hexdigest()
    if signature == sha1Str:
        return True
    else:
        return False

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
    scope = 'snsapi_base'
    state = 'dengyh'
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?'
    queryString = urllib.urlencode({
        'appid' : appid,
        'redirect_uri' : redirect_uri,
        'response_type' : response_type,
        'scope' : scope,
        'state' : state,
        })
    return url + queryString

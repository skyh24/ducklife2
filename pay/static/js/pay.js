var timeStamp = "";
var nonceString = "";
var packageString = "";
var paySignString = "";
var appid = ""; // 必填
var appkey = ""; //必填
var partnerId = ""; //必填
var partnerKey = ""; //必填


function getTimeStamp() {
    if (timeStamp == "") {
        timeStamp = new Date().getTime().toString();
    }
    return timeStamp;
}

function getNonceStr() {
    if (nonceString == "") {
        var $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var maxPos = $chars.length;
        for (i = 0; i < 32; i++) {
            nonceString += $chars.charAt(Math.floor(Math.random() * maxPos));
        }
    return nonceString;
}

function getSignType() {
    return "SHA1";
}

function getPackage(dict) {
    if (packageString == "") {
        var packageList = [];
        var packageUrlList = [];
        for (var item in dict) {
            packageList.push(item + '=' + dict[item]);
            packageUrlList.push(item + '=' + encodeURIComponent(dict[item])).replace(/%[0-9A-F]{2}/g, function(code) {
                return code.toLowerCase();
            });
        }
        packageUrlList.sort();
        packageList.sort();
        var string1 = packageList.join('&');
        var string2 = packageUrlList.join('&');
        var stringSignTemp = string1 + '&key=' + partnerKey;
        var signValue = CryptoJS.MD5(stringSignTemp).toUpperCase();
        packageString = string2 + '&sign=' + signValue;
    }
    return packageString;
}

function getPaySign(dict) {
    if (paySignString == "") {
        var paySignList = [];
        for (var item in dict) {
            paySignList.push(item + '=' + dict[item]);
        }
        paySignList.sort();
        var string1 = paySignList.join('&');
        var paySign = $.encoding.digests.hexSha1Str(string1).toLowerCase();
        console.log(paySign);
    }
    return paySignString;
}

document.addEventListener('WeixinJSBridgeReady', function() {
    $('#confirmPayment').click(function() {
        WeixinJSBridge.invoke('getBrandWCPayRequest',
        {
            "timeStamp" : getTimeStamp(),
            "nonceStr" : getNonceStr(),
            "package" : getPackage({
                "bank_type" : "WX",
                "body" : "XXX",
                // "attach" : "test",
                "partner" : partnerid,
                "out_trade_no" : "16642817866003386000",
                "total_fee" : 1,
                "fee_type" : 1,
                "notify_url" : "http://www.qq.com",
                "spbill_create_ip" : "127.0.0.1",
                "input_charset" : "GBK",
            }),
            "signType" : getSignType({
                "appId" : appid,
                "timeStamp" : 189026618,
                "nonceStr" : "adssdasssd13d",
                "package" : packageTmp,
                "signType" : "SHA1",
                "paySign" : paySign,
            }),
            "paySign" : getSign()
        }, function() {
            if (res.err_msg == "get_brand_wcpay_request: ok") {

            }
        });
    });
    WeixinJSBridge.log('ok');
}, false);
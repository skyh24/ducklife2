from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('order.views',
    url(r'^$', 'order_view', {'templateName' : 'order.html'}),
    url(r'^havepay/$', 'havepay_view', {'templateName' : 'havepay.html'}),
    url(r'^havecancel/$', 'havecancel_view', {'templateName' : 'havecancel.html'}),
    url(r'^create/$', 'create_order'),
    url(r'^cancel/$', 'cancel_order'), # for ajax
)

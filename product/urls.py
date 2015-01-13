from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('product.views',
    url(r'^$', 'index_view', {'templateName' : 'index.html'}),
    url(r'^cart/$', 'cart_view', {'templateName' : 'cart.html'}),
    url(r'^kefu/$', 'kefu_view'),
    url(r'^(\d+)/product/$', 'product_view', {'templateName' : 'product.html'}),
    url(r'^product/(\d+)/$', 'product_detail_view', {'templateName' : 'product_detail.html'}),
    url(r'^clear/$' ,'clear_cart'), # for ajax
    url(r'^add/$', 'add_product'), # for ajax
    url(r'^address/$', 'add_address'),
    url(r'^reduce/$', 'reduce_product'), # for ajax
    url(r'^cancel/$', 'cancel_product'), # for ajax
)

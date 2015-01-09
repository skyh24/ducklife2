from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('backend.views',
    url(r'^$', 'backend_view', {'templateName' : 'backend.html'}),
    url(r'^create/category/$', 'create_category'), # for ajax
    url(r'^create/product/$', 'create_product'), # for ajax
    url(r'^delete/product/$', 'delete_product'), # for ajax
    url(r'^delete/category/$', 'delete_category'), # for ajax
    url(r'^delivery/order/$', 'delivery_order'), # for ajax
    url(r'^cancel/order/$', 'cancel_order'), # for ajax
    url(r'^paid/order/$', 'paid_order'), # for ajax
    url(r'^upload/$', 'upload_pictures'), # for ajax
)

from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('pay.views',
	url(r'^payment/$', 'payConfirm_view', {'templateName' : 'pay_confirm.html'}),
)

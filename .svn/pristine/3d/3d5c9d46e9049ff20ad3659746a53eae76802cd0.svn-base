from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('product.urls')),
    url(r'', include('base.urls')),
    url(r'^pay/', include('pay.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^backend/', include('backend.urls')),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {
        'document_root' : settings.PROJECT_PATH
        }),
)

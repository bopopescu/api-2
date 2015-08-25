# coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin: 
from django.contrib import admin  
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('web_mgr.urls')),
    url(r'^accounts/login/$', include('web_mgr.urls')),
    url(r'^web_mgr/', include('web_mgr.urls')),
    url(r'^data_mgr/', include('data_mgr.urls')),
    url(r'^exception_mgr/', include('exception_mgr.urls')),

    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()

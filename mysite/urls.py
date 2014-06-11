from django.conf.urls import patterns, include, url
from django.contrib import admin
from xml_parse import urls

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^xmls/', include('xml_parse.urls')),
)

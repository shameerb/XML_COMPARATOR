from django.conf.urls import patterns, include, url
from xml_parse import views

urlpatterns = patterns('',
	url(r'^$', views.all_xml_obj,name='all_xml_obj'),
	url(r'^(?P<xml_id_1>\d+)_(?P<xml_id_2>\d+)/$', views.xml_obj,name='xml_obj'),
	url(r'^(?P<xml_id>\d+)/details_ob1/$', views.details_ob1,name='details_ob1'),
	url(r'^(?P<xml_id>\d+)/details_ob2/$', views.details_ob2,name='details_ob2'),
	url(r'^(?P<xml_id_1>\d+)_(?P<xml_id_2>\d+)/xml_diff/$', views.xml_diff,name='xml_diff'),
	url(r'^(?P<xml_id_1>\d+)_(?P<xml_id_2>\d+)/xml_copy/$', views.xml_copy,name='xml_copy'),
	url(r'^ajax_json$', views.ajax,name='ajax_json'),
	#url(r'^ajax$', views.main,name='ajax'),
)
from django.shortcuts import render,get_object_or_404
from xml_parse.models import xml_object,xml_object_2
import xml_parse.xml_compare_changed as XC
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
import re


def all_xml_obj(request):
	xml_all_obj_1=xml_object.objects.all()
	xml_all_obj_2=xml_object_2.objects.all()
	similiar_list=[]
	difference_list=[]
	#improve logic for different number of elements in both list 
	for i in range(len(xml_all_obj_1)):
		obj1=xml_all_obj_1[i]
		obj2_list=xml_all_obj_2.filter(object_name=obj1.object_name)
		for k in obj2_list:
			obj2=k
		if str(obj1.xml)==str(obj2.xml):
			similiar_list.append({'object_name':obj1.object_name,'xml1':obj1.xml,'xml2':obj2.xml})
		else:
			difference_list.append({'object_name':obj1.object_name,'xml1':obj1.xml,'xml2':obj2.xml})
		
	return render(request,'all_xml_obj.html',{'similiar_list':similiar_list,'difference_list':difference_list})
	
def xml_obj(request,xml_id_1,xml_id_2):
	xml_obj_1=get_object_or_404(xml_object,id=xml_id_1)
	xml_obj_2=get_object_or_404(xml_object_2,id=xml_id_2)
	return render(request,'xml_obj.html',{'xml_obj_1':xml_obj_1,'xml_obj_2':xml_obj_2})

def details_ob1(request,xml_id):
	xml_obj=get_object_or_404(xml_object,id=xml_id)
	return render(request,'details.html',{'xml':xml_obj})

def details_ob2(request,xml_id):
	xml_obj=get_object_or_404(xml_object,id=xml_id)
	return render(request,'details.html',{'xml':xml_obj})
	
def xml_diff(request,xml_id_1,xml_id_2):
	xc_name,xc_diff=('','')
	xml_obj_1=get_object_or_404(xml_object,id=xml_id_1)
	xml_obj_2=get_object_or_404(xml_object_2,id=xml_id_2)
	xc_name,xc_diff=XC.xml_diff(xml_obj_1.object_name,xml_obj_1.xml,xml_obj_2.xml)
	# print 'xml_diff'
	# print xc_name,xc_diff
	# print 'xml_diff'
	return render(request,'xml_diff.html',{'xc_name':xc_name,'xc_diff':xc_diff})

def xml_copy(request,xml_id_1,xml_id_2):
	xml_obj_1=get_object_or_404(xml_object,id=xml_id_1)
	xml_obj_2=get_object_or_404(xml_object_2,id=xml_id_2)
	xml_obj_2.xml=xml_obj_1.xml
	xml_obj_2.save()
	return render(request,'xml_copy.html',{'xml_obj_1':xml_obj_1,'xml_obj_2':xml_obj_2})
 

def ajax(request):
	if request.POST.has_key('client_object_1'):
		xc_name=''
		xc_diff=''
		obj_1_id=request.POST['client_object_1']
		obj_2_id=request.POST['client_object_2']
		xml_obj_1=get_object_or_404(xml_object,id=obj_1_id)
		xml_obj_2=get_object_or_404(xml_object_2,id=obj_2_id)
		xc_name,xc_diff=XC.xml_diff(xml_obj_1.object_name,xml_obj_1.xml,xml_obj_2.xml)
		# print 'ajax'
		# print xc_name,xc_diff
		# print 'ajax'
		xc_diff=xc_diff.replace('<tab>','&emsp;')
		xc_diff=xc_diff.replace('<','&lt;')
		xc_diff=xc_diff.replace('>','&gt;')
		xc_diff=xc_diff.replace('[1]-','<code class="green">')
		xc_diff=xc_diff.replace('-[1]','</code>')
		xc_diff=xc_diff.replace('[2]-','<code class="red">')
		xc_diff=xc_diff.replace('-[2]','</code>')
		xc_diff=xc_diff.replace('!br!','<br>')
		# print 'ajax_2'
		# print xc_name,xc_diff
		# print 'ajax_2'
		response_dict={}
		response_dict.update({'xc_name': xc_name })
		response_dict.update({'xc_diff': xc_diff })
		return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
	else:
		return render_to_response('xml_obj.html', context_instance=RequestContext(request))
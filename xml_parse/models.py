from django.db import models

class xml_object(models.Model):
	object_name=models.CharField(max_length=200)
	xml=models.CharField(max_length=20000)
	
	def __unicode__(self):
		return self.object_name
	
class xml_object_2(models.Model):
	object_name=models.CharField(max_length=200)
	xml=models.CharField(max_length=20000)
	
	def __unicode__(self):
		return self.object_name
	
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Article(models.Model): 
	
	title = models.CharField(max_length= 200, blank= True, default= 'NO TITLE')
	description = models.CharField(max_length= 1000, blank= True, default= '')
	imageUrl = models.CharField(max_length= 1000, blank=True, default= '')
	link = models.CharField(max_length= 500, blank= False, default= '')
	bias = models.FloatField()
	created = models.DateTimeField(auto_now_add= True)

	class Meta: 
		ordering = ('created',)



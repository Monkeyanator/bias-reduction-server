# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Article(models.Model): 
	
	title = models.CharField(max_length= 200, blank= True, default= 'NO TITLE')
	description = models.CharField(max_length= 1000, blank= True, default= '')
	imageUrl = models.CharField(max_length= 1000, blank=True, default= '')
	link = models.CharField(max_length= 500, blank= False, default= '')
	bias = models.FloatField()
	created = models.DateTimeField(auto_now_add= True)

	class Meta: 
		ordering = ('created',)

class Clickthrough(models.Model): 

	created = models.DateTimeField(auto_now_add= True)
	user = models.ForeignKey(User)
	article = models.ForeignKey(Article)

	class Meta: 
		ordering = ('created',)
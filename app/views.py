# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions 
from app.serializers import ArticleSerializer, UserSerializer, ClickthroughSerializer
from app.models import Article, Clickthrough


class ArticleViewSet(viewsets.ModelViewSet): 
	queryset = Article.objects.all() 
	serializer_class = ArticleSerializer

class ClickthroughViewSet(viewsets.ModelViewSet): 
	queryset = Clickthrough.objects.all() 
	serializer_class = ClickthroughSerializer 
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer): 
		serializer.save(user= self.request.user)

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all() 
	serializer_class = UserSerializer
	model = User

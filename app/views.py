# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets 
from app.serializers import ArticleSerializer, UserSerializer
from app.models import Article


class ArticleViewSet(viewsets.ModelViewSet): 
	queryset = Article.objects.all() 
	serializer_class = ArticleSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all() 
	serializer_class = UserSerializer
	model = User

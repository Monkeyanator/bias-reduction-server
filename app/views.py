# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets 
from app.serializers import ArticleSerializer
from app.models import Article

class ArticleViewSet(viewsets.ModelViewSet): 
	queryset = Article.objects.all() 
	serializer_class = ArticleSerializer
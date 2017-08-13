# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, permissions 
from app.serializers import ArticleSerializer, UserSerializer, ClickthroughSerializer
from app.models import Article, Clickthrough

from prediction import UserBasedKNN

import os 
import csv

#-=-=-=-=-=-=-=-
#REST API default routes
#-=-=-=-=-=-=-=-

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



#-=-=-=-=-=-=-=-=-=-
#Prediction endpoints
#-=-=-=-=-=-=-=-=-=-

def user_based_knn(request, userId): 

	print "Recommendations for: ", userId 

	algo = UserBasedKNN(3)

	BASE = os.path.dirname(os.path.abspath(__file__))
	ARTICLE_CSV_PATH = os.path.join(BASE, 'clickthroughs.csv')

	algo.load_clickthrough_file(ARTICLE_CSV_PATH)
	recommendations = algo.recommend(int(userId), 3)

	articleIds = [recommendation[0] for recommendation in recommendations]

	return render_article_list(articleIds)


def render_article_list(articleIds):
	articleQueryset = Article.objects.filter(pk__in= articleIds)
	serializer = ArticleSerializer(articleQueryset, many= True)
	return JsonResponse(serializer.data, safe= False)

#-=-=-=-=-=-=-
#Data model updates 
#-=-=-=-=-=-=-

#route that will load our articles from csv file
def load_articles(request):
	BASE = os.path.dirname(os.path.abspath(__file__))
	ARTICLE_CSV_PATH = os.path.join(BASE, 'articles.csv')
	with open(ARTICLE_CSV_PATH, 'r') as articleFile: 
		reader = csv.reader(articleFile)
		for article in reader: 
    		
			if article[0] == 'Title': 
				continue

			_, a = Article.objects.get_or_create( 
				title= article[0], 
				description= article[1],
				imageUrl= article[2],
				link= article[3],
				bias= article[4]	
			)

	return HttpResponse(status= 201)
from rest_framework import serializers 
from app.models import Article

class ArticleSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Article 
        fields = ('id', 'title', 'description', 'imageUrl', 'link', 'bias')
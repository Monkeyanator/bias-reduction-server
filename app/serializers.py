from rest_framework import serializers 
from app.models import Article, Clickthrough
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Article 
        fields = ('id', 'title', 'description', 'imageUrl', 'link', 'bias')

class ClickthroughSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Clickthrough
        fields = ('id', 'user', 'article')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

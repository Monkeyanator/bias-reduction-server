from rest_framework import serializers 
from app.models import Article
from django.contrib.auth.models import User 

class ArticleSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Article 
        fields = ('id', 'title', 'description', 'imageUrl', 'link', 'bias')

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only= True)

    def create(self, validated_data): 
        
        user = User.objects.create(username= validated_data['username'])
        user.set_password(validated_data['password'])
        user.save() 

        return user 

    class Meta:
        model = User
        fields = ('id', 'username','password')
 		

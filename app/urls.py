from django.conf.urls import url 
from app import views 
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include 
from rest_framework.routers import DefaultRouter

router = DefaultRouter() 
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
]
from django.conf.urls import url 
from app.views import ArticleViewSet, UserViewSet, ClickthroughViewSet 
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter() 
router.register(r'articles', ArticleViewSet)
router.register(r'users', UserViewSet)
router.register(r'clickthroughs', ClickthroughViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),
]
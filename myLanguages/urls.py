"""myLanguages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from app import views
from rest_framework.authtoken import views as view_auth
from app.serializers import LanguageViewSet, LessonViewSet, CategoryViewSet, ResumedArticleWordViewSet, ArticleLessonViewSet

router = routers.DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'lesson-words', ResumedArticleWordViewSet)
router.register(r'lesson-articles', ArticleLessonViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-token-auth/', view_auth.obtain_auth_token),
    url(r'^get-token/', views.get_token, name='get-token'),
    url(r'^create-lessons/', views.CreateLessons, name='create-lessons'),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

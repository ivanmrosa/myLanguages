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
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from common import views
from vocplus.views import create_user, get_file_content
from vocplus.views import LanguageViewSet, WordViewSet, WordRankViewSet, \
  LessonViewSet, LessonWordViewSet, LessonMediaViewSet, UserComplementViewSet, \
  UserLearningLanguageViewSet, UserViewSet
 #from app.serializers import LanguageViewSet, LessonViewSet, CategoryViewSet, ResumedArticleWordViewSet, ArticleLessonViewSet

from rest_framework.authtoken import views as view_auth


router = routers.DefaultRouter()
router.register(r'language', LanguageViewSet)
router.register(r'word', WordViewSet)
router.register(r'word-rank', WordRankViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'lesson-word', LessonWordViewSet)
router.register(r'lesson-media', LessonMediaViewSet)
router.register(r'user-complement', UserComplementViewSet)
router.register(r'user-learning-language', UserLearningLanguageViewSet)
router.register(r'user', UserViewSet)
#router.register(r'lessons', LessonViewSet)
#router.register(r'categories', CategoryViewSet)
#router.register(r'lesson-words', ResumedArticleWordViewSet)
#router.register(r'lesson-articles', ArticleLessonViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-token-auth/', view_auth.obtain_auth_token),
    url(r'^get-token/', views.get_token, name='get-token'),
    url(r'^create-user/', create_user, name='create-user'),
    url(r'^get-file/$', get_file_content, name='get_file_content'),
    
    #url(r'^create-lessons/', views.CreateLessons, name='create-lessons'),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
] 

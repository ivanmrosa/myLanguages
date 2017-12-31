from rest_framework import serializers, viewsets
from app.models import Language, Lesson, ArticleLesson, ArticleWord, Category, ResumedArticleWord
from django.db.models import F


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    language_name = serializers.ReadOnlyField(source='language.name')
    class Meta:
        model = Lesson
        fields = ('id', 'date', 'language', 'language_name', 'language_id')

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'path_to_image')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer        


class ResumedArticleWordSerializer(serializers.HyperlinkedModelSerializer):
    word_identification = serializers.StringRelatedField(many=False)   
    class Meta:
        model = ResumedArticleWord
        fields = ('id', 'word_identification', 'repetitions',)

class ResumedArticleWordViewSet(viewsets.ModelViewSet):
    queryset = ResumedArticleWord.objects.all()
    filter_fields = ('word_identification','article__lesson_id', 'article__source_page_category__category_id')    
    serializer_class = ResumedArticleWordSerializer        


class ArticleLessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleLesson
        fields = ('id', 'link', 'title',)

class ArticleLessonViewSet(viewsets.ModelViewSet):
    queryset = ArticleLesson.objects.all()
    filter_fields = ('source_page_category__category_id', 'lesson_id')    
    serializer_class = ArticleLessonSerializer            
from rest_framework import serializers, viewsets
from vocplus.models import Language, Word, WordRank, Lesson, LessonWord, \
    LessonMedia, UserComplement, UserLearningLanguage
from django.db.models import F
from django.contrib.auth.models import User


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'active')


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'text')



class WordRankSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.ReadOnlyField(source='word.text')
    class Meta:        
        model = WordRank
        fields = ('id', 'position', 'text', 'word_id')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:        
        model = Lesson
        fields = ('id', 'name', 'sequence', 'language_id')



class LessonWordSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.ReadOnlyField(source='word.text')
    class Meta:        
        model = LessonWord
        fields = ('id', 'lesson_id', 'word_id', 'text')


class LessonMediaSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:        
        model = LessonMedia
        fields = ('id', 'lesson_id', 'media_type', 'subject', 'link')


class UserComplementSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:        
        model = UserComplement
        fields = ('id', 'user_id', 'official_language_id')


class UserLearningLanguageSerializer(serializers.HyperlinkedModelSerializer):    
    language_name = serializers.ReadOnlyField(source="language.name")
    lesson_sequence = serializers.ReadOnlyField(source="actual_lesson.sequence")
    class Meta:        
        model = UserLearningLanguage
        fields = ('id', 'user_id', 'language_id', 'actual_lesson_id', 'score', 'language_name', 'lesson_sequence', 'actual_lesson')
            

class UserSerializer(serializers.HyperlinkedModelSerializer):     
    password = serializers.CharField(write_only=True)
    class Meta:        
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user        


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from vocplus.models import Language, Word, WordRank, Lesson, LessonWord, \
    LessonMedia, UserComplement, UserLearningLanguage


from vocplus.serializer import LanguageSerializer, WordSerializer, WordRankSerializer, LessonSerializer, LessonWordSerializer, \
    LessonMediaSerializer, UserComplementSerializer, UserLearningLanguageSerializer, UserSerializer

# Create your views here.



@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()                

        #for now english will be default
        usr = dict(serialized.data)
        usr_id = usr["id"]
        lang_id = Language.objects.get(name='English - US').id
        less = Lesson.objects.get(sequence=1)
        UserComplement.objects.create(user_id=usr_id, official_language_id=lang_id).save()
        UserLearningLanguage.objects.create(user_id=usr_id, language_id=lang_id, actual_lesson_id=less.id, score=0).save()

        return Response(serialized.data, status=status.HTTP_201_CREATED)        
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    filter_fields = ('active',)    
    serializer_class = LanguageSerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    filter_fields = ('text',)    
    serializer_class = WordSerializer


class WordRankViewSet(viewsets.ModelViewSet):
    queryset = WordRank.objects.all()    
    serializer_class = WordRankSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()    
    filter_fields = ('id', 'sequence', 'language_id')
    serializer_class = LessonSerializer

class LessonWordViewSet(viewsets.ModelViewSet):
    queryset = LessonWord.objects.all()    
    filter_fields = ('id', 'lesson_id')
    serializer_class = LessonWordSerializer


class LessonMediaViewSet(viewsets.ModelViewSet):
    queryset = LessonMedia.objects.all()    
    filter_fields = ('id', 'lesson_id', 'media_type', 'subject')
    serializer_class = LessonMediaSerializer

class UserComplementViewSet(viewsets.ModelViewSet):
    queryset = UserComplement.objects.all()    
    filter_fields = ('id', 'user_id', 'official_language_id')
    serializer_class = UserComplementSerializer

class UserLearningLanguageViewSet(viewsets.ModelViewSet):
    queryset = UserLearningLanguage.objects.all()    
    filter_fields = ('id', 'user_id', 'language_id', 'user__username')
    serializer_class = UserLearningLanguageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()    
    filter_fields = ('id', 'username', 'email')
    serializer_class = UserSerializer

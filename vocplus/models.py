from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


MEDIA_TYPE = ( ('V', 'Video'), ('I', 'Image'), ('T', 'Text'), ('P', 'Podcast') )

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Language'    

class Word(models.Model):
    text = models.CharField(max_length=100, db_index=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']    
        db_table = 'Word'

class WordRank(models.Model):
    word = models.OneToOneField(Word)
    position = models.IntegerField(db_index=True)

    def __str__(self):
        return str(self.position) + ' - ' + self.word.text
    
    class Meta:
       ordering = ['position']
       db_table = 'WordRank'        

class Lesson(models.Model):
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=100)
    sequence = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Lesson'
        ordering = ['sequence']        

class LessonWord(models.Model):
    lesson = models.ForeignKey(Lesson, db_index=True)
    word = models.OneToOneField(Word)


    def __str__(self):
        return self.lesson.name + ' - ' + self.word.text

    class Meta:
        db_table = 'LessonWord'


class LessonMedia(models.Model):
    lesson = models.ForeignKey(Lesson, db_index=True)
    subject = models.CharField(max_length=100)
    media_type = models.CharField(max_length=1, choices=MEDIA_TYPE)
    link = models.URLField()


    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'LessonMedia'


class UserComplement(models.Model):
    user = models.OneToOneField(User)
    official_language = models.ForeignKey(Language)

    class Meta:
        db_table = 'UserComplement'
    
class UserLearningLanguage(models.Model):
    user = models.ForeignKey(User)
    language = models.ForeignKey(Language)
    actual_lesson = models.ForeignKey(Lesson)
    score = models.IntegerField()
    last_access = models.DateField(blank=True, null=True)
    classification = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'UserLearningLanguage'

    
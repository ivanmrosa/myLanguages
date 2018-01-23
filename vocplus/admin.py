from django.contrib import admin
from vocplus.models import Language, Word, Lesson, LessonWord, LessonMedia, UserComplement, UserLearningLanguage, WordRank
# Register your models here.
admin.site.register(Language)
admin.site.register(Word)
admin.site.register(WordRank)
admin.site.register(Lesson)
admin.site.register(LessonWord)
admin.site.register(LessonMedia)
admin.site.register(UserComplement)
admin.site.register(UserLearningLanguage)


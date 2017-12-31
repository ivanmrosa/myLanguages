from django.contrib import admin
#from rest_framework.authtoken.admin import TokenAdmin
from app.models import Language, Category, Word, Lesson, SourcePage, ArticleLesson, ArticleWord, SourcePageCategory, RegularExpression, ResumedArticleWord
# Register your models here.
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Word)
admin.site.register(Lesson)
admin.site.register(SourcePage)
admin.site.register(SourcePageCategory)
admin.site.register(ArticleLesson)
admin.site.register(ArticleWord)
admin.site.register(RegularExpression)
admin.site.register(ResumedArticleWord)
#TokenAdmin.raw_id_fields = ('user',)

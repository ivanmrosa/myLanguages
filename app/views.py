from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Count
from django.core.exceptions import ObjectDoesNotExist
from crawler.reader import PageReader
from app.models import Language, Category, Word, Lesson, SourcePage, \
    SourcePageCategory, ArticleLesson, ArticleWord, ResumedArticleWord
from datetime import date, datetime
import ast
import os.path
import re
import urllib
import requests
from rest_framework.exceptions import AuthenticationFailed



# Create your views here.


DELETE_CHARACTERS = (".", ",", ":", ";", "?", "!")

class LessonController(object):

    def __init__(self, use_log):
        self.__use_log = use_log
        self.__file_log = None
        self.__ignore_word_pattern = re.compile("\w")
        self.__created_lesson = None

    def __register_log(self, log_text):
        file_name = 'log.txt'
        if self.__use_log:
            if not self.__file_log:
                if os.path.exists(file_name):
                    mode = 'a'
                else:
                    mode = 'w'
                self.__file_log = open(file_name, mode)
            self.__file_log.write(str(datetime.now()) + ' - ' + log_text + '\n')

    def __finish_log(self):
        if self.__file_log:
            self.__register_log('finished')
            self.__file_log.close()

    def __new_lesson(self, language_id):
        if self.__created_lesson == None:
            le = Lesson(language_id=language_id, date=date.today())
            le.save()
            self.__created_lesson = le
        
        return self.__created_lesson


    def __get_page_articles(self, page_category_dict):
        if page_category_dict["list_regex_get_links"]:
            reader = PageReader(
                link=page_category_dict["link"],
                list_regex_to_links = ast.literal_eval(page_category_dict["list_regex_get_links"]),
                list_regex_to_title = ast.literal_eval(page_category_dict["list_regex_get_title"]),
                list_regex_to_article = ast.literal_eval(page_category_dict["list_regex_get_article"])
            )
        else:
            reader = PageReader(
                list_regex_to_links = ast.literal_eval(page_category_dict["list_regex_get_links"]),
                list_regex_to_title = ast.literal_eval(page_category_dict["list_regex_get_title"]),
                list_regex_to_article = ast.literal_eval(page_category_dict["list_regex_get_article"])
            )

        return reader.get_data()

    def __new_article_lesson(self, link, title, source_page_category_id, lesson_id):
        art = ArticleLesson(
            link = link,
            title = title,
            source_page_category_id = source_page_category_id,
            lesson_id = lesson_id
        )
        art.save()
        return art

    def __get_word_id(self, word_text):
        word_cap = word_text.lower().capitalize()
        word = Word.objects.filter(word = word_cap).values_list('id')
        if word:
            return word[0][0]
        else:
            w = Word(word = word_cap)
            w.save()
            return w.id

    def __ignored_word(self, word_text):
        if len(word_text) > 30 or not word_text or \
            self.__ignore_word_pattern.search(word_text):
            return True

        return False

    def __get_checked_word(self, word_text):
        word = word_text.strip()

        if word:
            for ch in DELETE_CHARACTERS:
                word = word.replace(ch, "")

        return word

    def __new_article_word(self, article_id, word_text, position):
        word = self.__get_checked_word(word_text)

        if self.__ignored_word(word):
            return None

        word_id = self.__get_word_id(word_text=word)

        aw = ArticleWord(
            article_id = article_id,
            word_identification_id = word_id,
            position = position
        )

        try:
            aw.save()
        except Exception as e:
            raise Exception('Exception at article\' word creating. Word id: ' + str(word_id)  + ' ' + str(e))
        return aw

    def __insert_many_articles(self, article_data, source_page_category_id,
        lesson_id):
        if article_data:
            self.__register_log('inserting articles')

        for article in article_data:

            article_lesson_id = self.__new_article_lesson(article["link"],
                article["title"], source_page_category_id, lesson_id).id
            position = 0
            if article["words"]:
                self.__register_log('inserting words')
            for word in article["words"]:
                position += 1
                self.__new_article_word(article_id = article_lesson_id,
                    word_text = word, position= position)


    def __create_article_lesson(self, id_language=None, id_category=None):
        if id_language:
            languages = Language.objects.get(pk=id_language).values('id')
        else:
            languages = Language.objects.values('id')

        for lang in languages:
            self.__register_log('Starting Language ' + str(lang["id"]))

            if id_category:
                filter = {"main_source_page__language__id":lang["id"], \
                    "category_id": id_category}
            else:
                filter = {"main_source_page__language__id":lang["id"]}

            lesson = self.__new_lesson(lang["id"])

            source_page_categories = SourcePageCategory.objects.\
                    annotate(
                       list_regex_get_links=F('regular_expression__list_regex_get_links'),
                       list_regex_get_title=F('regular_expression__list_regex_get_title'),
                       list_regex_get_article=F('regular_expression__list_regex_get_article')
                ).filter(**filter).values()

            for source_page in source_page_categories:
                self.__register_log('Starting source page category ' + str(source_page["id"]))
                articles_data = self.__get_page_articles(source_page)
                self.__insert_many_articles(articles_data, source_page["id"],
                    lesson.id)
    
    def insert_resumed_words(self, lesson_id=None):
        lesson_key = None
        if not lesson_id and self.__created_lesson:            
            lesson_key = self.__created_lesson
        elif lesson_id:
            lesson_key = lesson_id
        
        if lesson_key:
            articles_words = ArticleWord.objects.filter(article__lesson__id=lesson_key).values('article_id', 'word_identification__id').\
            annotate(num_words=Count('word_identification__id'))
            for article_word in articles_words:
               resume = ResumedArticleWord(article_id=article_word['article_id'], word_identification_id=article_word['word_identification__id'],
                  repetitions=article_word['num_words'])
               resume.save()



    def CreateLessons(self, id_language=None, id_category=None):
        try:
            self.__register_log('Initializing')
            self.__create_article_lesson(id_language=id_language, id_category=id_category)
            self.insert_resumed_words()
        finally:
            self.__finish_log()


def CreateLessons(request):
    begin_time = datetime.now()
    lessons = LessonController(use_log=True)
    lessons.CreateLessons()
    end_time = datetime.now()

    return HttpResponse('Lições criadas: Inicio: %s, Fim: %s' % (str(begin_time), str(end_time)))


def get_token(request):
    client_id = request.POST.get('client')
    client_secret = request.POST.get('secret')
    user = request.POST.get('username')
    password = request.POST.get('password')
    grant_type = request.POST.get('grant_type')
    data = {'grant_type':grant_type, 'username':user, 'password':password}
    server_url = request.META["HTTP_HOST"]
    url = 'http://' + client_id + ':' + client_secret + '@' + server_url + '/o/token/'  # 'localhost:8000/o/token/'
    with requests.post(url, data) as f:                
        return HttpResponse(f.text, status=f.status_code)
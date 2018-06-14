
import sys, os, django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR) #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myLanguages.settings")
django.setup()



from common.views import ReaderFile, ReaderCSV
from vocplus.models import Word, Language, WordRank, Lesson, LessonWord
from django.utils.translation import gettext as _
import os


class WordUpload(object):
    def upload_words_from_file(self, language_name, reader_instance):
        assert isinstance(reader_instance, ReaderFile)        
        lang = Language.objects.get(name=language_name)
        line = reader_instance.get_next_line()         
        while line:
            if Word.objects.filter(language = lang, text = line[1]).count() == 0:
                w = Word.objects.create(language = lang, text = line[1])
                WordRank.objects.create(word = w, position=line[0])

            line = reader_instance.get_next_line()
        
        reader_instance.unload()


class LessonUpload(object):
    def create_lessons(self, language_name, words_per_lesson=20, start_at_word=None):
        lang = Language.objects.get(name=language_name)
        if start_at_word:
            wrid = WordRank.objects.get(text=start_at_word).id
            wr = WordRank.objects.filter(id__gte=wrid)
        else:
            wr = WordRank.objects.all()
        
        words_in_lesson = 0
        lessons_created = 0  

        for w in wr:
            if words_in_lesson >= words_per_lesson or words_in_lesson == 0:
                lessons_created += 1
                words_in_lesson = 0
                lesson = Lesson.objects.create(language=lang, name=_('Lesson') + ' ' + str(lessons_created), sequence=lessons_created)            
            
            LessonWord.objects.create(lesson=lesson, word_id=w.word_id)
            words_in_lesson += 1

                

def upload_word_from_file():
    csv = input('please, select the csv file...')
    language = input('please, type the language name...')
    if not os.path.exists(csv):
        raise FileExistsError("The selected file doesn't exists")
    reader = ReaderCSV(separator=';', path=csv)
    up = WordUpload() 
    up.upload_words_from_file(language_name=language, reader_instance=reader)


def upload_lessons():
    language = input('please, type the language name...')
    start_at_word = input('please, type the word the lessons must begin...')
    words_per_lesson = input('please, type the word per lessons...')
    lup = LessonUpload()
    lup.create_lessons(language_name = language, words_per_lesson=int(words_per_lesson), start_at_word=start_at_word)

def run():
    if sys.argv[1] == 'upcsv':
        upload_word_from_file()
    elif sys.argv[1] == 'uples':
        upload_lessons()


run()
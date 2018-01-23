from django.test import TestCase, Client
from vocplus.models import Language, Word, WordRank, Lesson, LessonWord, LessonMedia
import json
# Create your tests here.
class LanguangeTestCase(TestCase):
    def setUp(self):
        Language.objects.create(name="English")

    def test_insert_language(self):
        english = Language.objects.get(name="English")
        self.assertEqual(english.name, 'English')
    
    def test_edit_language(self):
        language = Language.objects.get(name="English")
        language.name = "English modified"
        language.save()
        eng = Language.objects.get(name='English modified')
        self.assertEqual(eng.name, 'English modified')
    
    def test_delete_language(self):
        eng = Language.objects.filter(name='English')
        eng.delete()
        eng_count = Language.objects.filter(name='English')
        self.assertEqual(eng_count.count(), 0)
    
    def test_get_language(self):
        c = Client()
        
        response = c.post('/get-token/', {
            "grant_type": "password",
            "username": 'outro',
            "password": 'vaitomarnocu',
            "client": 'XbTDHY3LxgjtBTnQp6OMIofIJo3xepNJXm59YHdg',
            "secret": 'jJmEHxAPxrYbj7H0YRUrTWI5wPvtuoVi5FrgfmM9FTnm9Mvn8PajXgx5VwKi2EjsVNA3cnQ4vAxzdPIz5OcAZmFyRnqa3yHFtWmlHEG0IAvbrHQLXEpLKvxB9aCHVLNF'
        })
        
        self.assertEqual(response.status_code, 200)        
        tk = response.json()["access_token"]
        
        response = c.get('/languages/', {}, **{"Authorization":' Bearer ' + tk})
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.content.json()["name"], 'English')

class WordTestCase(TestCase):
    def setUp(self):
        lang = Language.objects.create(name="English")
        Word.objects.create(language=lang, text="abc")

    def test_insert_word(self):
        word = Word.objects.get(text='abc')
        self.assertEqual(word.text, 'abc')
    
    def test_edit_word(self):
        word = Word.objects.get(text="abc")
        word.text = 'def'
        word.save()
        word = Word.objects.get(text='def')
        self.assertEqual(word.text, 'def')
    
    def test_delete_word(self):
        Word.objects.filter(text='abc').delete()                 
        self.assertEqual(Word.objects.filter(text='abc').count(), 0)        

class WordRankTestCase(TestCase):
    def setUp(self):
        WordTestCase().setUp()
        w = Word.objects.get(text="abc")
        WordRank.objects.create(word=w, position=1)

    def test_insert_word_rank(self):
        wr = WordRank.objects.get(word__text = 'abc')
        self.assertEqual(wr.word.text, 'abc')
    
    def test_edit_word_rank(self):        
        wr = WordRank.objects.get(word__text='abc')
        wr.position = 2
        wr.save()
        self.assertEqual(WordRank.objects.get(word__text='abc').position, 2)
    
    def test_delete_word_rank(self):
        WordRank.objects.filter(word__text='abc').delete()
        self.assertEqual(WordRank.objects.filter(word__text='abc').count(), 0)



class LessonTestCase(TestCase):
    def setUp(self):
        LanguangeTestCase().setUp()
        lan = Language.objects.get(name='English')
        Lesson.objects.create(language=lan, name='lesson 1', sequence=1)

    def test_insert_lesson(self):
        wr = Lesson.objects.get(name = 'lesson 1')
        self.assertEqual(wr.name, 'lesson 1')
    
    def test_edit_lesson(self):        
        wr = Lesson.objects.get(name='lesson 1')
        wr.name = 'lesson 2'
        wr.save()
        self.assertEqual(Lesson.objects.filter(name='lesson 2').count(), 1)
    
    def test_delete_word_rank(self):
        Lesson.objects.filter(name='lesson 1').delete()
        self.assertEqual(Lesson.objects.filter(name='lesson 1').count(), 0)


class LessonWordTestCase(TestCase):

    def setUp(self):
        LessonTestCase().setUp()
        le = Lesson.objects.get(name='lesson 1')
        WordTestCase().setUp()
        w = Word.objects.get(text='abc')
        LessonWord.objects.create(lesson = le, word=w)
    
    def test_insert_lesson_word(self):
        wr = LessonWord.objects.get(word__text = 'abc')
        self.assertEqual(wr.word.text, 'abc')
    
    def test_edit_lesson_word(self):        
        pass
        #wr = LessonWor].objects.get(word__text='abc')
        #wr.name = 'lesson 2'
        #wr.save()
        #self.assertEqual(Lesson.objects.filter(name='lesson 2').count(), 1)
    
    def test_delete_word_rank(self):
        LessonWord.objects.filter(word__text='abc').delete()
        self.assertEqual(LessonWord.objects.filter(word__text='abc').count(), 0)

class LessonMediaTestCase(TestCase):

    def setUp(self):
        LessonTestCase().setUp()
        le = Lesson.objects.get(name='lesson 1')
        LessonMedia.objects.create(lesson = le, subject='test', media_type=0)
    
    def test_insert_lesson_media(self):
        wr = LessonMedia.objects.get(subject = 'test')
        self.assertEqual(wr.subject, 'test')
    
    def test_edit_lesson_word(self):        
        pass
        wr = LessonMedia.objects.get(subject = 'test')
        wr.subject = 'test1'
        wr.save()
        self.assertEqual(LessonMedia.objects.get(subject = 'test1').subject, 'test1')
    
    def test_delete_word_rank(self):
        LessonMedia.objects.filter(subject='test').delete()
        self.assertEqual(LessonMedia.objects.filter(subject='test').count(), 0)




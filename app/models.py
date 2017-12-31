from django.db import models

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    path_to_image = models.CharField(max_length=100, verbose_name="Caminho para a imagem.", blank=False, null=True)
    def __str__(self):
        return self.name

class Word(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['word']

class Lesson(models.Model):
    language = models.ForeignKey(Language)
    date = models.DateField()

    def __str__(self):
        return str(self.date) + ' - ' + self.language.name


class RegularExpression(models.Model):
    name = models.CharField(max_length=50)
    list_regex_get_links = models.TextField(verbose_name="Gravar uma lista python com os regex para pegar os links",null=True, blank=True)
    list_regex_get_title = models.TextField(verbose_name="Gravar uma lista python com os regex para pegar o titulo do artigo")
    list_regex_get_article = models.TextField(verbose_name="Gravar uma lista python com os regex para o artigo")

    def __str__(self):
        return self.name


class SourcePage(models.Model):
    name = models.CharField(max_length=50)
    language = models.ForeignKey(Language)
    main_link = models.URLField()

    def __str__(self):
        return self.name


class SourcePageCategory(models.Model):
    main_source_page = models.ForeignKey(SourcePage)
    category = models.ForeignKey(Category)
    link = models.URLField()
    regular_expression = models.ForeignKey(RegularExpression, null=True, blank=False)

    def __str__(self):
        return self.main_source_page.name + ' - ' + self.category.name

class ArticleLesson(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=200)
    source_page_category = models.ForeignKey(SourcePageCategory)
    lesson = models.ForeignKey(Lesson)

    def __str__(self):
        return self.title + ' - '+ self.lesson.language.name + ' - ' + str(self.lesson.date)


class ArticleWord(models.Model):
    article = models.ForeignKey(ArticleLesson)
    word_identification = models.ForeignKey(Word)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.article.title + ' - ' + self.word_identification.word


class ResumedArticleWord(models.Model):
    article = models.ForeignKey(ArticleLesson)
    word_identification = models.ForeignKey(Word)
    repetitions = models.IntegerField()

    def __str__(self):
        return self.article.title + ' - ' + self.word_identification.word
    
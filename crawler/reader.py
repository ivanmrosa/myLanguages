from urllib import request
import re



class PageReader(object):
    def __init__(self, link, list_regex_to_links, list_regex_to_title, list_regex_to_article):
        self.__step_find_link = list_regex_to_links
        self.__step_find_title = list_regex_to_title
        self.__step_find_article = list_regex_to_article
        self.__link = link

    def get_page_html(self, link, encode_inf):
        with request.urlopen(link) as f:
            text = f.read().decode(encode_inf)
        return text

    def __execute_regex(self, list_text, regex):
        result = []
        for text in list_text:
            got = re.findall(regex, text, re.DOTALL)
            for item in got:
                if type(item) == tuple:
                    a = ""
                    for x in item:
                      a += x
                    result.append(a)
                else:
                    result.append(item)
        return result

    def get_links(self):
        html = self.get_page_html(self.__link, 'utf-8')
        if self.__step_find_link:
            result = [html]
            for regex in self.__step_find_link:
                result = self.__execute_regex(result, regex)
            return result
        return [self.__link]

    def get_data(self):
        html = ""
        article = []
        title = []
        result = []
        links = self.get_links()

        for link in links:
            html = self.get_page_html(link, 'utf-8')
            article = [html]
            title = [html]

            for regex in self.__step_find_article:
                article = self.__execute_regex(article, regex)

            for regex in self.__step_find_title:
                title = self.__execute_regex(title, regex)

            if article:
                article = article[0]
            if title:
                title = title[0]

            if article:
                result.append({"link": link, "title": title, "words":article.split(" ")})
        return result

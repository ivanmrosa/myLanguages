import os, abc
from django.shortcuts import render
from django.http import HttpResponse
import requests
# Create your views here.


class ReaderFile(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, separator, path):
        pass

    @abc.abstractmethod
    def unload(self):
        pass
    
    @abc.abstractmethod
    def get_line(self, line_pos):
       pass
    
    @abc.abstractmethod
    def get_field_on_line(self, line_pos, field_name):
        pass
    
    @abc.abstractmethod
    def get_next_line(self):
        pass


class ReaderCSV(ReaderFile):
    def __init__(self, separator, path):
        self.__separator = separator
        self.__path = path
        self.__file = None
        self.__field_map = {}
        self.__actual_read_line = 1

        self.__load()

    def __open_file(self):
        self.__file = open(self.__path, 'r')
    
    def __close_file(self):
        self.__file.close()
    
    def __map_fields(self):
        self.__open_file()
        header = self.__file.readlines(1)[0].split(self.__separator)
        count = 0
        for field in header:
            self.__field_map.update({field:count})
            count += 1
    
    def __load(self):
        self.__open_file()
        self.__map_fields()

    def __get_field_pos(self, field_name):
        return self.__field_map[field_name]

    def unload(self):
        self.__close_file()
    
    def get_line(self, line_pos=None):
        if line_pos:
            self.__file.seek(0, 0)
            for i  in range(0, line_pos):
                self.__file.__next__()
        
        line = self.__file.readline()
        
        if line:
            return line
        else:
            return None

    def __get_splited_fields(self, line_pos=None):
        line = self.get_line(line_pos)
        if line:
            return line.split(self.__separator)
        else:
            return None

    
    def get_field_on_line(self, line_pos, field_name):        
        fields = self.__get_splited_fields(line_pos)
        if fields:
            return fields[self.__get_field_pos(field_name)]
        else:
            return None

    def get_next_line(self):
       return self.__get_splited_fields()

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
        return HttpResponse(f.text, status=f.status_code, content_type="application/json")



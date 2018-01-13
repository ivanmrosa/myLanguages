import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   
class Config(object):
    @staticmethod
    def getAllowedHosts():
        return ['138.197.93.56']

    @staticmethod
    def getDatabaseConfig():
        ''' return {
                 'default': {
                     'ENGINE': 'django.db.backends.postgresql',
                     'NAME': 'mydatabase',
                     'USER': 'mydatabaseuser',
                     'PASSWORD': 'mypassword',
                     'HOST': '127.0.0.1',
                     'PORT': '5432',
                 }
         }'''

        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
           }
        }

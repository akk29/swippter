from django.contrib.auth.backends import ModelBackend

class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self,request,**kwargs):
        pass
from app.pattern.singleton import SingletonPattern

class BaseDAO(SingletonPattern):

    def __init__(self, model):
        self.model = model    

    def create(self,*args,**kwargs):
        pass

    def update(self,*args,**kwargs):
        pass

    def delete(self,*args,**kwargs):
        pass

    def fetch(self,*args,**kwargs):
        pass
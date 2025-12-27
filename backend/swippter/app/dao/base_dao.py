from app.pattern.singleton import SingletonPattern

class BaseDAO(SingletonPattern):

    def __init__(self, model):
        self.model = model    

    def create(self,**data):
        self.model.objects.create(**data)

    def update(self,filter,data):
        pass

    def delete(self,*args,**kwargs):
        pass

    def fetch(self,offset,limit,filters,projections):
        pass

    def count(self,filters):
        return self.model.objects.filter(**filters).count()
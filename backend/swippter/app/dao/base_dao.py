from app.pattern.singleton import SingletonPattern
from app.core.exceptions import NotFoundError


class BaseDAO(SingletonPattern):

    def __init__(self, model):
        self.model = model

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, data, **filter):
        self.model.objects.filter(**filter).update(**data)

    def delete(self, *args, **filter):
        self.model.objects.delete(**filter)

    def fetch(self, limit=None, offset=None, *projections, **filters):
        query = self.model.objects.filter
        if limit and offset:
            return query(**filters).values(*projections)[offset : offset + limit]
        return query(**filters).values(*projections)

    def fetch_one(self, msg=None, raise_error=False, **filters):
        try:
            data = self.model.objects.get(**filters)
            if data:
                return data
        except:
            if(raise_error):
                raise NotFoundError(msg=msg)
            return None

    def count(self, **filters):
        return self.model.objects.filter(**filters).count()

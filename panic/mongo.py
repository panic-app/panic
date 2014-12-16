from datetime import datetime

from mongoengine import StringField, BooleanField, queryset_manager, DateTimeField, Document
from mongoengine.connection import _get_db
import pymongo


class BaseDocument(Document):

    meta = {'abstract': True}

    created_on = DateTimeField(default=datetime.utcnow())

    @classmethod
    def find_by_id(cls, id):
        return cls.objects.with_id(id)

    @classmethod
    def exists(cls, **kwargs):
        results = cls.objects(**kwargs)
        if len(results) > 0:
            return True
        else:
            return False

    @classmethod
    def find_one(cls, **kwargs):
        return cls.objects(**kwargs).first()

    @classmethod
    def all(cls):
        return cls.objects().all()

    @classmethod
    def count_list(cls, document_id, list_field_name):
        """ counts number of items in a list.

        useful if you need to count the number of items in an large embedded list but
        you don't want to load the whole document into memory.

        args:
            document id: ObjectId of the document you're looking for
            list_field_name: name of the field where the list is. ex: keyword_targets for a Package document.
        """

        pipeline = [{'$match': {'_id': {'$in': [document_id]}}}, {"$unwind": "${}".format(list_field_name)},
                    {"$group": {"_id": "$_id", "count": {"$sum": 1}}}]
        result = cls._get_collection().aggregate(pipeline)['result']
        return result[0]['count']


class EnumField(StringField):

    def __init__(self, values, *args, **kwargs):

        if 'error' in values:
            raise AttributeError('error is a reserved mongo work -- sorry!')

        self.values = values
        super(EnumField, self).__init__(*args, **kwargs)

    def validate(self, value):
        if value not in self.values:
            self.error('Invalid Enum {} is not in {}'.format(str(value), self.values))

    def __getattr__(self, item):
        if item in self.values:
            return item
        else:
            raise AttributeError('')


from mongoengine import (
    Document,
    FloatField,
    StringField,
    URLField,
)


class Posting(Document):
    meta = {'collection': 'postings'}

    data_id = StringField(required=True, unique=True, max_length=20)
    url = URLField(required=True)
    latitude = FloatField()
    longitude = FloatField()

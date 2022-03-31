from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import News

@registry.register_document
class NewsDocument(Document):
    id = fields.IntegerField()

    class Index:
        name = 'news'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
        }

    class Django:
        model = News
        fields = [
            'description',
            'author',
            'keywords',
            'text',
            'title',
            'url',
            'parent_url',
            'publisheddate',
            'datemodified'
        ]


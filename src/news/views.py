# This is a sample Python script.
import json

from bs4 import BeautifulSoup
import requests
import pandas as pd


API_KEY = 'AIzaSyBuB7xqx1gX4RZX45kGgGwybifCgKzYa0A'
EMAIL = 'willems@ornicogroup.co.za'
PASSWORD = 'Subscriptions@123'

from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    NewsSerializer,
)
from .models import News
import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from .documents import NewsDocument

class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)

class SearchNews(PaginatedElasticSearchAPIView):
    serializer_class = NewsSerializer
    document_class = NewsDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'description',
                    'author',
                    'keywords',
                    'text',
                    'title',
                    'url',
                    'parent_url'
                ])

    #fuzziness = 'auto'

class NewsViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    # MultiPartParser AND FormParser
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    # "You will typically want to use both FormParser and MultiPartParser
    # together in order to fully support HTML form data."
    # parser_classes = (MultiPartParser, FormParser)
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permissions = {'default': (IsAuthenticated,)}


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
# This is a sample Python script.

# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

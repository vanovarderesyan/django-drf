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


def get_id_token():
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + API_KEY

    payload = {
        "returnSecureToken": "true",
        "email": EMAIL,
        "password": PASSWORD
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['idToken']

def parse_xml(xml_data):
    # Initializing soup variable
    soup = BeautifulSoup(xml_data, 'xml')

    # Creating column for table
    df = pd.DataFrame(columns=['description', 'author', 'keywords', 'publisheddate', 'datemodified', 'text','title', 'url'])

    # Iterating through item tag and extracting elements
    all_items = soup.find_all('loc')
    items_length = len(all_items)

    for index, item in enumerate(all_items):
        loc = item.text

        # Adding extracted elements to rows in table

        xml_data_loc = requests.get(loc).content
        soup_loc = BeautifulSoup(xml_data_loc, 'xml')
        all_items_loc = soup_loc.find_all('loc')
        items_length_loc = len(all_items_loc)

        id_token = get_id_token()
        for index_loc, item_loc in enumerate(all_items_loc):
            headers_get = {
                '24uat': id_token
            }
            httm_data_loc = requests.request("GET", 'https://www.news24.com/news24/southafrica/news/exclusive-mpofu-found-guilty-of-ethical-breach-for-telling-le-roux-to-shut-up-mulls-legal-challenge-20220315', headers=headers_get)
            soup_html = BeautifulSoup(httm_data_loc.text, 'html.parser')
            body = soup_html.find('div',{'class':'article__body'}).text
            description = soup_html.find('meta',attrs={"property": "og:description"}).get('content')
            title = soup_html.find('title').text

            author = soup_html.find('meta',attrs={"name": "author"}).get('content')
            keywords = soup_html.find('meta',attrs={"name": "keywords"}).get('content')
            publisheddate = soup_html.find('meta',attrs={"name": "publisheddate"}).get('content')
            datemodified = soup_html.find('meta',attrs={"name": "datemodified"}).get('content')
            body = body
            row = {
                'description': description,
                'author': author,
                'keywords': keywords,
                'publisheddate': publisheddate,
                'datemodified': datemodified,
                "text" : body,
                "title":title,
                "url" : 'https://www.news24.com/news24/southafrica/news/exclusive-mpofu-found-guilty-of-ethical-breach-for-telling-le-roux-to-shut-up-mulls-legal-challenge-20220315'

            }

            print(row)
            break

        df = df.append(row, ignore_index=True)
        print(f'Appending row %s of %s' % (index + 1, items_length))
        break

    return df

def main():
    url= 'https://www.news24.com/sitemap'
    xml_data = requests.get(url).content
    df = parse_xml(xml_data)
    # Use a breakpoint in the code line below to debug your script.
    df.to_csv('news.csv')


# Press the green button in the gutter to run the script.
# This is a sample Python script.
import json

from bs4 import BeautifulSoup
import requests
import pandas as pd
from .models import News
API_KEY = 'AIzaSyBuB7xqx1gX4RZX45kGgGwybifCgKzYa0A'
EMAIL = 'willems@ornicogroup.co.za'
PASSWORD = 'Subscriptions@123'
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_id_token():
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + API_KEY

    payload = {
        "returnSecureToken": "true",
        "email": EMAIL,
        "password": PASSWORD
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['idToken']

def parse_xml(xml_data):
    # Initializing soup variable
    soup = BeautifulSoup(xml_data, 'xml')
    # Iterating through item tag and extracting elements
    all_items = soup.find_all('loc')
    items_length = len(all_items)

    for index, item in enumerate(all_items):
        loc = item.text

        # Adding extracted elements to rows in table

        xml_data_loc = requests.get(loc).content
        soup_loc = BeautifulSoup(xml_data_loc, 'xml')
        all_items_loc = soup_loc.find_all('loc')
        items_length_loc = len(all_items_loc)
        id_token = get_id_token()
        for index_loc, item_loc in enumerate(all_items_loc):
            url = item_loc.text

            headers_get = {
                '24uat': id_token
            }
            try:
                httm_data_loc = requests.request("GET", url, headers=headers_get)
                soup_html = BeautifulSoup(httm_data_loc.text, 'html.parser')
                body = soup_html.find('div',{'class':'article__body'}).text
                description = soup_html.find('meta',attrs={"property": "og:description"}).get('content')
                title = soup_html.find('title').text

                author = soup_html.find('meta',attrs={"name": "author"}).get('content')
                keywords = soup_html.find('meta',attrs={"name": "keywords"}).get('content')
                publisheddate = soup_html.find('meta',attrs={"name": "publisheddate"}).get('content')
                datemodified = soup_html.find('meta',attrs={"name": "datemodified"}).get('content')
                body = body

                News.objects.create(
                    description=description,
                    author=author,
                    keywords=keywords,
                    publisheddate=publisheddate,
                    datemodified=datemodified,
                    text=body,
                    title=title,
                    url=url,
                    parent_url=loc
                )
            except:
                pass


            # break


    return True

def main():
    url= 'https://www.news24.com/sitemap'
    xml_data = requests.get(url).content
    parse_xml(xml_data)



# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

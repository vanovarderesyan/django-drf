import json

from bs4 import BeautifulSoup
import requests
from .models import News,ScrapConfig
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
                if News.objects.filter(url=url).exists():
                    print('update',url)
                    News.objects.filter(url=url).update(
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
                else:
                    print('creta',url)

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
                print('err')
                pass


            # break


    return True

def main():
    # if ScrapConfig.objects.filter(started=True).exists():
    #     return
    ScrapConfig.objects.filter().update(started=True)
    url= 'https://www.news24.com/sitemap'
    xml_data = requests.get(url).content
    parse_xml(xml_data)
    ScrapConfig.objects.filter().update(started=False)


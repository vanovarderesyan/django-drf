from rest_framework.routers import SimpleRouter

from .views import (
    NewsViewset
)

# import requests
#
# url = "https://www.clevescene.com/cleveland/Rss.xml"
#
# payload={}
# headers = {
#     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
# }
#
# response = requests.request("GET", url, headers=headers, data=payload)
#
# print(response.text)


app_router = SimpleRouter()

app_router.register(r'news', NewsViewset,basename='News')


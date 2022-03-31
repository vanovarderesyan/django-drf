from django.db import models

# Create your models here.
'description', 'author', 'keywords', 'publisheddate', 'datemodified', 'text','title', 'url'

class News(models.Model):
    description = models.TextField(null=True,blank=True)
    author = models.TextField(null=True,blank=True)
    keywords = models.TextField(null=True,blank=True)
    publisheddate = models.CharField(null=True,blank=True,max_length=500)
    datemodified = models.CharField(null=True,blank=True,max_length=500)
    text = models.TextField(null=True,blank=True)
    title = models.TextField(null=True,blank=True)
    url = models.URLField(null=True,blank=True,unique=True)
    parent_url  = models.URLField(null=True,blank=True)


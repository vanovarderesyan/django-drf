from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .views import main
from .models import News

# main()

@admin.register(News)
class newsAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'keywords', 'publisheddate', 'datemodified','title', 'url','parent_url')


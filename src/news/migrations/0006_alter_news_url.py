# Generated by Django 3.2.12 on 2022-03-29 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_news_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]
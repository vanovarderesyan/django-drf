# Generated by Django 3.2.12 on 2022-03-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20220322_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.TextField(blank=True, null=True),
        ),
    ]

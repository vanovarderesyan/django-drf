# Generated by Django 3.2.12 on 2022-03-22 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=500, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('publisheddate', models.CharField(blank=True, max_length=500, null=True)),
                ('datemodified', models.CharField(blank=True, max_length=500, null=True)),
                ('text', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
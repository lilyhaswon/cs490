# Generated by Django 3.2.8 on 2021-12-21 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chkboxcourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursename', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GetArticles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=1000)),
                ('urlToImage', models.CharField(max_length=1000)),
                ('publishedAt', models.CharField(max_length=1000)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
    ]

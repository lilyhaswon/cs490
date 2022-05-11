from django.db import models

class chkboxcourse(models.Model):#checkbox
    coursename = models.CharField(max_length=100)#checkbox


class GetArticles(models.Model): #news api database 
    author          = models.CharField(max_length=1000)
    title           = models.CharField(max_length=1000)
    description     = models.CharField(max_length=1000)
    url             = models.CharField(max_length=1000)
    urlToImage      = models.CharField(max_length=1000)
    publishedAt     = models.CharField(max_length=1000)
    content         = models.CharField(max_length=1000)

from django.shortcuts import render #goes to the template and takes stuff from the template

from preference.models import GetArticles
import requests #pip request
API_KEY = 'beb15e285be24fc281451991a011e116' # token for news api KH

# def home_view(request):
#     keyword = request.GET.get('keyword') #search
#     category = request.GET.get('category') #click
    
#     #in the url path the part &sortBy=-publishedAt sorts the articles, now the most recent pops up 
#     if keyword:#when there is a keyword in the seach bar (user wrote a keyword to search)
#         url = f'https://newsapi.org/v2/everything?pageSize=5&sortBy=-publishedAt&q={keyword}&apiKey={API_KEY}'
#         response = requests.get(url)
#         data = response.json() 
#         articles = data['articles']

#     elif category:#when there is a category (click on the anchor tags)            
#         url = f'https://newsapi.org/v2/top-headlines?pageSize=5&sortBy=-publishedAt&country=us&category={category}&apiKey={API_KEY}'
#         response = requests.get(url)
#         data = response.json()
#         articles = data['articles']

#     else:#when your on the home page and there isn't a selected category or search
#         url = f'https://newsapi.org/v2/top-headlines?pageSize=5&sortBy=-publishedAt&country=us&category=general&apiKey={API_KEY}'
#         response = requests.get(url)
#         data = response.json()
#         articles = data['articles']

#     context = {
#        'articles' : articles
#     }

#     return render(request, "preference_links/home.html",context)

# def profile_view(request):
#     context = {}
#     return render(request, "preference_links/profile.html",context)

def home_view(request):
    category = request.GET.get('category') #click

    if category:#when there is a category (click on the anchor tags)            
        url = f'https://newsapi.org/v2/top-headlines?pageSize=5&sortBy=-publishedAt&country=us&category={category}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']

    else:#when your on the home page and there isn't a selected category or search
        url = f'https://newsapi.org/v2/top-headlines?pageSize=5&sortBy=-publishedAt&country=us&category=general&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']

    context = {
       'articles' : articles
    }

    return render(request, "preference_links/home.html",context)

def profile_view(request):
    context = {}
    return render(request, "preference_links/profile.html",context)

#live searches 
def news(request): 
    category = request.GET.get('category') #click

    if category:#when there is a category (click on the anchor tags)            
        url = f'https://newsapi.org/v2/top-headlines?pageSize=5&sortBy=-publishedAt&country=us&category={category}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']

    else:#when your on the home page and there isn't a selected category or search
        url = f'https://newsapi.org/v2/top-headlines?pageSize=5&sortBy=-publishedAt&country=us&category=general&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']

    context = {
       'articles' : articles
    }

    return render(request, 'preference_links/news.html', context) 

from preference.models import chkboxcourse

# converts news api json to python objects(lists), then put them into database 
def saveArticle(request):
    keyword = request.GET.get('keyword') #search
    if request.method == "GET":
        if keyword: #click
            url = f'https://newsapi.org/v2/everything?pageSize=2&sortBy=-publishedAt&q={keyword}&apiKey={API_KEY}'
            response = requests.get(url)
            data = response.json()
            for art in data['articles']: #articles is the directory folder
                saveArt = GetArticles() #in models.py 
                saveArt.author = art['author'] #author is a list, the author not in '' is the name of the column in the database 
                saveArt.title = art['title'] #title is a list 
                saveArt.description = art['description']
                saveArt.url = art['url']
                saveArt.urlToImage = art['urlToImage']
                saveArt.publishedAt = art['publishedAt']
                saveArt.content = art['content']
                saveArt.save() #save to database 
            return render(request,'preference_links/home.html')
        else:
            return render(request,'preference_links/home.html')
    else:
        return render(request,'preference_links/home.html')



#user choosing there own tabs, not working at the moment 
def savevalues(request):
    if request.method == "POST":
        if request.POST.get('coursename'):
            savedata = chkboxcourse()
            savedata.coursename = request.POST.get('coursename')
            savedata.save()
            return render(request,'preference_links/profile.html')
    else:
            return render(request,'preference_links/profile.html')
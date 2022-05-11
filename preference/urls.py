from django.urls import path 
from preference.views import news #function in views.py 

urlpatterns = [         
    path('', news, name='news'),#makes search work  
]

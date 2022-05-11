"""kalApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include # calling other urls.py in other folders 
from django.contrib.auth import views as auth_views # don't know, but it works for change password

from preference.views import(home_view, profile_view,savevalues,saveArticle) # real home page 
from forms_and_logic.views import (registration_view,
                                  reset_view,
                                  login_view,
                                  logout_view,
                                  password_change_success_view,
                                  account_search_view,
                                  account_view,
                                  ) 


urlpatterns = [

    #Rest API Framework urls, file urls.py in forms_and_logic api folder 
    path('api/', include('forms_and_logic.api.urls')),

    #path('', home_view, name = "home"),# real home page 
    path('', saveArticle, name = "home"),# work in progress  
    path('profile/',profile_view, name = "profile"),#place for users to edit there account like change password
    path('save/',savevalues, name = "save"), # to save user picked options 

    path('account/',account_view, name = "forms_and_logic"),#place for users to edit there account like change password

    path('register/', registration_view, name = "register-form"), # new users 
    path('reset/', reset_view, name = "reset-form"),  #change passwords 
    path('login/', login_view, name = "login-form"), #login goes to home 
    path('logout/', logout_view, name = "logout-form"), #logout goes to home   
    
    path('friend/',include ('friendship.url', namespace ='friend')), #this will be the page to see your friends
    path('news/', include('preference.urls')), #get ya news from preference folder
	path('search/', account_search_view,name="search"), # New url for account_search_view
    path('forms_and_logic/', include('forms_and_logic.urls', namespace='forms_and_logic')),

    path('admin/', admin.site.urls),# change password only works when having this 
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name = "form_links/reset.html"), name = "change_password"), #django's defualt change password 
    path('password_change_success/', password_change_success_view, name = "password_change_done"), #redrict back to home.html

]

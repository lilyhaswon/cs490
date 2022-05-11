from django.urls import path # for path to link up with urls.py in kalApp folder 
from rest_framework.authtoken.views import obtain_auth_token #restframe's default token stuff 

from forms_and_logic.api.views import (
    api_display_register_info, # get method, showing the api for register info
    registration_view, # post method, creates new users for the database   
    api_update_register_info, #edit current user accounts 
    api_delete_register_info, #efit current user accounts 
    )



app_name = 'api'# name is linked to the urls.py in the kalApp folder

# only Rest API Framework urls
urlpatterns = [
    path('register-details/',api_display_register_info, name ="register-form-details"), #get request, showing whats in the register
    path('register-details-update',api_update_register_info, name ="register-form-update"),
    path('register-details-delete',api_delete_register_info, name ="register-form-delete"),

    #when using post,put or delete method, do not put a slash like register/, no '/'
    path('register', registration_view, name = "register-form"), # same path as the register.html, but this one wil use postman.com to made new users 
    path('login', obtain_auth_token, name = "login"), # token for logging in, it looks for the email 
]
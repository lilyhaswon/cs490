from django.core.exceptions import ValidationError # error alerts to users
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager # djando imports, to edit the default user model

from django.conf import settings # for token
from django.db.models.signals import post_save #for token
from django.dispatch import receiver #for token
from rest_framework.authtoken.models import Token #for token 

class MyAccountManager(BaseUserManager): #has to have BaseUserManager when not matching to django defaults data model fields 
    #for normal users 
    def create_user(self,email,username,password = None): # have all the current fields, self is the required to use AbstractBaseUser stuff
        if not email:
            raise ValidationError("User must have an email address") 
        if not username:
            raise ValidationError("User must have an username")
        
        # when users do have an username and email, then data is passed to database 
        user = self.model(
            email = self.normalize_email(email), #converts all email to lower case
            username = username,
        )

        user.set_password(password) # set_password is in BaseUserManger class 
        user.save(using = self._db) # save user to the database, using,s is a keyword 
        return user
    
    #users that can look at database called superusers
    def create_superuser(self,email,username,password):
        user = self.create_user( # calling self.model in class create_user
            email = self.normalize_email(email),
            password = password,
            username = username,
        )

        # changing the defaults in Account class
        user.is_admin = True  
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser): # the database 
    email                   = models.EmailField(unique = True, verbose_name = 'email') # verbose_name is just change table name to email
    username                = models.CharField(max_length=10, unique = True)
    data_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add = True)#requied to use AbstractBaseUser, auto_now_add will automaticaly add date user is created
    last_login              = models.DateTimeField(verbose_name='last login', auto_now = True)#requied to use AbstractBaseUser, auto_now will automaticly update each time user is logged in
    is_admin                = models.BooleanField(default=False)#requied to use AbstractBaseUser
    is_active               = models.BooleanField(default=True)#requied to use AbstractBaseUser
    is_staff                = models.BooleanField(default=False)#requied to use AbstractBaseUser
    is_superuser            = models.BooleanField(default=False)#requied to use AbstractBaseUser

    USERNAME_FIELD = 'email' # able to login with only email, USERNAME is a keyword in django
    REQUIRED_FIELDS = ['username'] #list of requied items

    objects = MyAccountManager() # tells the Account class where the manger is, which is in class MyAccountManager

    def __str__(self): # things to be displayed on the testhome.html page
        return self.email + " , " + self.username # will display as email,username
    
    def has_perm(self, perm , obj = None):#required to build a custom user model
        return self.is_admin
    
    def has_module_perms(self, app_label):#required to build a custom user model
        return True

#will be a POST for tokens
@receiver(post_save, sender = settings.AUTH_USER_MODEL)# in kalApp folder file settings.py has AUTH_USER_MODEL
def create_auth_token(sender, instance = None, created = False, **kwargs):#when a new user is created, a token will also be created for each user
    if created:
        Token.objects.create(user = instance)


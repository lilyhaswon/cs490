# all the columns in the database 
from django import forms 
from django.contrib.auth.forms import UserCreationForm # built in class from django, helps to creating form fields 
from django.contrib.auth import authenticate # django default for login users 

from forms_and_logic.models import Account #cutom made in model.py 

class RegisterationForm(UserCreationForm): #django default for building registeration froms 
    email = forms.EmailField(help_text='')#help_text will display next to the email 

    class Meta: # what the form will look like, as in what fields it has 
        model = Account 
        fields = ('email','username','password1','password2')


class AccountAuthenticationForm(forms.ModelForm): # custom to check users when they log in 
    
    password = forms.CharField(label = "Password",widget=forms.PasswordInput) #django's default password

    class Meta: #login expected fields 
        model = Account 
        fields = ('email','password')
    
    def clean(self): #clears the form before each use
        if self.is_valid(): # when form loads 
            email = self.cleaned_data['email'] 
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password): # checking password in database is equal to the user's input
                raise forms.ValidationError("Email or password is wrong") # for other errors that is not field input
        











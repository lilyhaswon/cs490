#serializers are used for geting and posting stored data such as fields in the database 
from rest_framework import serializers #django's resetframe work defaults 

from forms_and_logic.models import Account # in models.py 


#turns database info for registeration into a json format 
class DisplayRegisterSerializer(serializers.ModelSerializer): # a get request to show who is registered  
    class Meta:
        model = Account 
        fields = ['email','username','password'] # items being printed in json format


class CreateRegistrationSerializer(serializers.ModelSerializer): #can create new users using postman.com 

    # password2 is not a django default field, so this line create one for password2 
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only = True) #write_only hides the password

    class Meta:
        model = Account
        fields = ['email','username','password','password2'] #password is password1, django's default has it named password 
        
        #extra rules for each field 
        extra_kwargs = {
            'password':{'write_only' : True}
        }
    
    #overwriting the save method in dejango's defaults, so password and password2 is the same passowrd
    def save(self):
        account = Account( # post email and username to the database 
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        #before posting password and password2 check is both passwords are the same 
        if password != password2:
            raise serializers.ValidationError({'password' : 'Passwords must match.'})
        account.set_password(password) #post password into database 
        account.save() # since we are overwriting django's default save method, we add this to save it 
        return account 
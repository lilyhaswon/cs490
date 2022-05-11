from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.authtoken.models import Token # when the page fails to load use a 404 page 
from rest_framework.response import Response #django's resetframe work defaults 
from rest_framework.decorators import api_view #django's resetframe work defaults 

from forms_and_logic.models import Account # the model being used to get registeration info 
from forms_and_logic.api.serializers import DisplayRegisterSerializer #from serializers.py 
from forms_and_logic.api.serializers import CreateRegistrationSerializer

from rest_framework.authtoken.models import Token #for token 
from rest_framework.decorators import permission_classes #permission tokens 
from rest_framework.permissions import IsAuthenticated #permission tokens


@api_view(['GET',]) # can only use a get request 
@permission_classes((IsAuthenticated,)) #must have permission tokens to view this path
def api_display_register_info(request): 

    try:
        userAccountInfo = Account.objects.all() #contains all email, username and password from the database, when they registered to the site 
    except Account.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND) # page error when page fails to load 
    
    if request.method == "GET": # extra get just in case a POST makes it in 
        serializer = DisplayRegisterSerializer(userAccountInfo, many = True) # get the data from the database, many means all the items 
        return Response(serializer.data) #prints data in json format, can be viewed using url path to it

@api_view(['POST',]) # only post request
def registration_view(request):

    if request.method == 'POST': # can be deleted, sometimes the other @api_view affect everthing, makes sure its a post request 
        serializer = CreateRegistrationSerializer(data = request.data)
        data = {} # works like context = {} in other views.py files 
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user." # message if new user is created 
            data['email'] = account.email #shows the upload email is json format, only in postman.com
            data['username'] = account.username
            token = Token.objects.get(user = account).key #get token from database 
            data['token'] = token #post token into json thing
        else:
            data = serializer.errors # shows the error message in serializers.py 
        return Response(data)# passing data to the database 


num = 3 # id column in database, manually have to change row number for edits for update and delete 

@api_view(['PUT',])# only can use put requests
def api_update_register_info(request):  # for updataiang current users info, only using postman.com

    try:
        userAccountInfo = Account.objects.get(pk = num) #contains all email, username and password from the database
    except Account.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND) # page error when page fails to load 
    
    if request.method == "PUT": # extra put just in case other requests affect it  
        serializer = DisplayRegisterSerializer(userAccountInfo,data = request.data) # gets the items from the database 
        data = {}
        if serializer.is_valid(): # when all info is vaild 
            serializer.save()
            data["success"] = "update successful."
            return Response(data = data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) #when the info is wrong, gets this error reply


@api_view(['DELETE',])#only can use delete requests 
def api_delete_register_info(request): # for deleting current users info, only using postman.com

    try:
        userAccountInfo = Account.objects.get(pk = num) #contains all email, username and password from the database
    except Account.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND) # page error when page fails to load 
    
    if request.method == "DELETE": # extra delete just in case other requests affect it  
        operation = userAccountInfo.delete()
        data = {}
        if operation: # when delete is successful 
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data = data) 


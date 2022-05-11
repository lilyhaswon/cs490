from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect #change link address 
from django.contrib.auth import login,authenticate,logout # django defaults 

from django.shortcuts import render, redirect
from forms_and_logic.models import Account
from forms_and_logic.forms import RegisterationForm #custom made in forms.py, registering users 
from forms_and_logic.forms import AccountAuthenticationForm # in forms.py, for logging in users 
from django.http import HttpResponse #people search allows a http respose 
#LH bit
from friendship.views import FriendRequestStatus, get_friend_request_or_false #its the checks that the ifs in the otherProfile.html are checking for like 
from friendship.models import FriendList, FriendRequest 



def registration_view(request): #registerating 
    context = {} #populate with info

    if request.POST:
        form = RegisterationForm(request.POST) #variable now holds username,email,password,verifiyPassword
        if form.is_valid(): # when there is no errors with user input, so form will be saved 
            form.save() # form is now saved
            email = form.cleaned_data.get('email')# get email from the form 
            raw_password = form.cleaned_data.get('password1')# get password from the form 
            # django's defaults for checking for a good password 
            account = authenticate(email = email, password = raw_password) #creates user object to be and replace the django defaults of email and password
            login(request,account) #will log in the user 
            return redirect('home') # after submiting form user will go back to the home page
        else: # when form is not vailed 
            context['registration_form'] = form # passing to a template named registration_form
    else: #when theres a get request
        form = RegisterationForm()
        context['registration_form'] = form    

    return render(request, "form_links/register.html",context)# return to the register page 

def login_view(request):#populate resgisterating ino
    context = {}

    user = request.user 
    if user.is_authenticated: # when its a vaild user redirect to home page
        return redirect("home") 
    if request.POST: 
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid(): 
            email = request.POST['email'] 
            password = request.POST['password']
            user = authenticate(email=email, password=password)# when password and email is correct 

            if user: 
                login(request,user) #logs in the user 
                return redirect("home") #back to home page

    else:
        form = AccountAuthenticationForm() # the raw form, meaning no one log in yet 
    context['login_form'] = form # in login.html there a line that connect to this, makes the feilds appear for the form  
    return render(request, "form_links/login.html",context) 

def logout_view(request):  #sends back to home page
    logout(request) 
    return redirect("home") #sends back to home page

def reset_view(request):
    context = {}
    return render(request, "form_links/reset.html",context)

def password_change_success_view(request): # page after user changed password 
    return redirect("home")

#KH bit
#this is the friend search bar 
def account_search_view(request, *args, **kwargs): #this is how we search for friendship
	context = {} #this is what will come back
	if request.method == "GET":  #did the user search anything in friendship bar?
		search_query = request.GET.get("q") # q is what the user is searching in the firendship bar 
		if len(search_query) > 0: # there is a file in the friendship app called views.py at the very bottom I put what each of the numbers mean (sent a request, got one, neither sent)
			search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
                        #from def account get objects and filter them by user name(and email) but don't show multiples(distinct of username) (both the email and user as seperate accounts in case their username and email is the same)icontains is it doesn't matter if its caps or lowercase
			user = request.user 
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results: #returns the query set of matching search results
				accounts.append((account, False)) # you have no friends yet cause we don't have friends yet
			context['accounts'] = accounts #list = accounts
				
	return render(request, "form_links/search_results.html", context)
    #starts a query to find future friend it should look for the forms and logic app and go into the templates and find search_results its in the templates/form_links

def get_redirect_if_exists(request): #it gives our list of potential friends on kalApp
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def account_view(request, *args, **kwargs): 
	"""
	- 
		is_self (boolean)
			is_friend (boolean) --> labels in friendship.views(at the very bottom)
			  -1: NO_REQUEST_SENT 
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id) #using the user_id created in the logic_and_forms.viwe file as a marker 
	except:
		return HttpResponse("Something went wrong. couldn't get the primary key userid from the account.objects...") #where did we go? 
	if account:
        #our labels to find people
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends

		# Define template variables
		is_self = True # we are ourselves
		is_friend = False #we shouldn't be our friend
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
		friend_requests = None
		user = request.user #so who are we friend or self?
		if user.is_authenticated and user != account: #if we are logged in but the profile we are lookingat isn't ours
			is_self = False # we are not ourself
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
			if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
			elif get_friend_request_or_false(sender=user, receiver=account) != False:
				request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
			# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
			else:
				request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

		elif not user.is_authenticated: #your not even logged in...
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_Active = True)
			except:
				pass
			
		# Set the template variables to the values
		context['is_self'] = is_self #different types on info for if your are yourself 
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		return render(request, "form_links/otherProfile.html", context) #this is the view of someones account.... it nees to go to form_links because thats where the otherprofile.html is :(



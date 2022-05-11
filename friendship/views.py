from django.shortcuts import render #gives us the stack to actually send string around
from django.http import HttpResponse #send the link/payload
import json
from enum import Enum  #they all have to unique values
from forms_and_logic.models import Account#gives us the account models with info to use
from friendship.models import FriendRequest, FriendList #gives us 

def friends_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("That user does not exist.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Could not find a friends list for {this_user.username}")
			
	return render(request, "friendship_links/friend_list.html", context)

def send_friend_request(request): # we are sending the friend request
	user = request.user #us user is the varaible to represent what we did
	payload = {} 
	if request.method == "POST" and user.is_authenticated: # get what they sent if we are logged in 
		user_id = request.POST.get("receiver_user_id") #what we get back is what our protental friend will use as a unique identifier
		if user_id: #if they are logged in we check... 
			receiver = Account.objects.get(pk=user_id) # we label them as athe receiver in our relation of 
			try:
				# Get any friend requests (active and not-active)
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active (pending)
				
				try:
					for request in friend_requests:
						raise Exception("You already following them.")

					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Following!."

				except Exception as e:
					payload['response'] = str(e)
					
			except FriendRequest.DoesNotExist: # there wasn't a already pending request
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None: 
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request." #something went wrong... but we are not going to tell them
	else: #somehow they are able to see another proflie page and sees a friend button when they are not logged in
		payload['response'] = "You must be authenticated (logged in) to follow someone."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def friend_requests(request, *args, **kwargs): #status of the follow
	return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_friend(request, *args, **kwargs):
	user = request.user 
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that follow."  #a mistake in case something went wrong specifically about the friend request being sent
	else:
		# should never happen 
		payload['response'] = "You must be authenticated to remove a follow." #how dare you remove your friend
	return HttpResponse(json.dumps(payload), content_type="application/json") #okay we are now updating the fact you've removed your friend from your friendlist

def get_friend_request_or_false(sender, receiver): #was there a friend request sent or not?? --> looks for if anyone sent a friend request 
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver,is_active=True) #someone did send a friendrequest
    except FriendRequest.DoesNotExist: #no one sent a friend request
        return False

def cancel_friend_request(request, *args, **kwargs): #this doesn't work
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
			except FriendRequest.DoesNotExist:
				payload['response'] = "Nothing to cancel. Friend request does not exist."

			# There should only ever be ONE active friend request at any given time. Cancel them all just in case.
			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cance()
				payload['response'] = "Friend request canceled."
			else:
				# found the request. Now cancel it
				friend_requests.first().cancel()
				payload['response'] = "Friend request canceled."
		else:
			payload['response'] = "Unable to cancel that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to cancel a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

class FriendRequestStatus(Enum): #fixed and are the only cases that can happen
    NO_REQUEST_SENT = -1 # neither of the users sent a follow request
    THEM_SENT_TO_YOU = 0 # the act of seeing a friend request
    YOU_SENT_TO_THEM = 1 # the act of sending a friend request
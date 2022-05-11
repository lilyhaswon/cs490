from django.contrib import admin
from friendship.models import FriendRequest, FriendList

class FriendListAdmin(admin.ModelAdmin):
	list_filter = ['user'] #potentally find friends in list
	list_display = ['user'] #show our friends
	search_fields = ['user'] #look for more friends
	readonly_fields = ['user'] #what can we see from our friends or someone else's page


admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
	list_filter 	= ['sender', 'receiver']
	list_display 	= ['sender', 'receiver']

	search_fields 	= ['sender__username', 'sender__email','receiver_email','receiver_username'] 
	#we cannot search with objects (which is what account profile is made of so we have to use the email or infomation in database)
	#__ is to select a specific field inside the sender or receiver

	class Meta:
		model = FriendRequest
admin.site.register(FriendRequest, FriendRequestAdmin)


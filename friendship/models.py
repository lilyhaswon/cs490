from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch.dispatcher import receiver #standard

import forms_and_logic #they couldn't find account from the next line so I added this so the code can find account
from forms_and_logic.models import Account #we need to find ourselves
from django.conf import settings #get the settings
from django.utils import timezone #get time

# Create your models here.

class FriendList(models.Model): #saving stuff
    user    =   models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
                                     #you need to be real,  we need to be able to remove friends, they are named user
   # bio     =   models.textfield() #extra points hopefully

    friends =   models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'friends', blank=True)
                                    #friend need to be real,  we need to be able to find friends, blank = true cause its possible to have no friends :(
    def __str__(self):
        return self().user.username

    def add_friend(self):
        if not forms_and_logic in self.friends.all(): #if they are not in our friendlist --searches forms_and_logic-friendlist for if they are already friend
            self.friends.add(forms_and_logic) #add to our account
            self.save #save the friends
    
    def remove_friend(self):
        if forms_and_logic in self.friends.all(): #if they are not in our friendlist --searches forms_and_logic-friendlist for if they are already friend
            self.friends.add(forms_and_logic) #add to our forms_and_logic
            self.save

    def unfriend(self,removee): #our friend unfriending us 
        remover_friends_list = self #the friendship destoryer --one doing unfriending
        remover_friends_list.remove_friend(removee)  # -its the action of unfriending by friendship destoryer on their side
        
        #we are deleting ourself from their friendlist
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)#we are gone from their friendlist

    def is_mutual_friend(self,friend): #are we even friends? both friends
        if friend in self.friends.all(): # checks if friend is in our friendlist
            return True #if they are its true
        return False #other wise its false T-T

class FriendRequest(models.Model): #the bits and bops that make a friend request happen labeling stuff
    #theres a couple steps in becoming friends #relationship
     #1 sender- person sending and starting the friendship request
     #2 receiver-person getting the friendship request
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="receiver")

    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self): #accept friend request of accepted so we add to our and their friendlist
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender) #receiver accepts so update their friendlist
            sender_friend_list= FriendList.objects.get(user=self.sender) #sender gets friend
            
            if sender_friend_list: #we are now friends so we update their friendlist
                sender_friend_list.add_friend(self.receiver)
                self.is_action = False
                self.save()
    
    def decline(self): #they/we rejected friendship
        self.is_active = False
        self.save()
    
    def cancel(self):#we decided to cancel the friend request we are making a notification
        self.is_active = False
        self.save()
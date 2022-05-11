from django.urls import path
from friendship.views import(
    send_friend_request,
    friend_requests,
    #not made remove_friend,
    FriendRequest,
    friends_list_view
)

app_name="friendship" 

urlpatterns = [
    path('friend_request/', send_friend_request, name = "friend-request"),
    
    path('friend_requests/<user_id>/', friend_requests, name='friend-requests'),

    path('list/<user_id>', friends_list_view, name='list'),
]
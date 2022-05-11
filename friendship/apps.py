from django.apps import AppConfig


class FriendshipConfig(AppConfig):
    name = 'friendship'

    def read(self):
        import friendship.signals
        #get the created signals.py

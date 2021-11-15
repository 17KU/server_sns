from django.conf.urls import url
from .views import AddFriend
from .views import ShowFriend
from .views import AddFavorite
from .views import DeleteFriend
from .views import findChat

urlpatterns = [
    url('add_friend', AddFriend.as_view(), name ='add_friend'),
    url('show_friend', ShowFriend.as_view(), name ='show_friend'),
    url('add_favorite', AddFavorite.as_view(), name ='add_favorite'),
    url('delete_friend', DeleteFriend.as_view(), name = 'delete_friend'),
    url('find_chat', findChat.as_view(), name = 'find_chat')
]
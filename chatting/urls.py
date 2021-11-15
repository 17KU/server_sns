from django.conf.urls import url
from .views import ChatListSelect
from .views import ChatListInsert
from .views import ChatListDelete

urlpatterns = [
    url('chat_list_select', ChatListSelect.as_view(), name='chat_list_select'),
    url('chat_list_insert', ChatListInsert.as_view(), name='chat_list_insert'),
    url('chat_list_delete', ChatListDelete.as_view(), name='chat_list_delete')
]

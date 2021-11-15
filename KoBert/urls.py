from django.conf.urls import url
from .views import GetEmotion

urlpatterns = [
    url('get_emotion', GetEmotion.as_view(), name='get_emotion')
]
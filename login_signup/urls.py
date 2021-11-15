from django.conf.urls import url
from .views import UserRegist
from .views import UserDupliCheck
from .views import UserLogin
from .views import UserPwdChange
from .views import UserNameChange


urlpatterns = [
    url('user_regist', UserRegist.as_view(), name = 'user_regist'),
    url('user_dupli_check', UserDupliCheck.as_view(), name = 'user_dupli_check'),
    url('user_login', UserLogin.as_view(), name = 'user_login'),
    url('user_pwd_change', UserPwdChange.as_view(), name = 'user_pwd_change'),
    url('user_name_change', UserNameChange.as_view(), name = 'user_name_change')
]
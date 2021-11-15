from django.db import models
from login_signup.models import User

class Chat(models.Model):
    chat_index = models.AutoField(primary_key=True)
    chat_title = models.CharField(max_length=200, null=False, default=False)
    chat_other_id = models.CharField(max_length=256, null=False, default=False)

    class Meta :
        db_table = 'chat'
        verbose_name = '채팅 목록'

class User_Chat(models.Model):
    uc_chat_index = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False, default=False, db_column='uc_chat_index')
    uc_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=False, db_column='uc_user_id')

    class Meta :
        db_table = 'user_chat'
        verbose_name = '유저-채팅 테이블'



from django.db import models
from login_signup.models import User
from chatting.models import Chat
# Create your models here.

class Msg(models.Model):
    msg_index = models.AutoField(primary_key=True)
    msg_chat_index = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False, default=False, db_column='msg_chat_index')
    msg_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=False, db_column='msg_user_id')
    msg_datetime = models.DateTimeField(auto_now_add=True)
    msg_text = models.TextField()
    msg_emo_name = models.CharField(max_length=256, null=False, default=False)


    class Meta:
        db_table = 'msg'
        verbose_name = '메세지 테이블'
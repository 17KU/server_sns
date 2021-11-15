from django.db import models
from login_signup.models import User

# Create your models here.

class user_friend(models.Model):

    uf_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default = False, db_column='uf_user_id')
    uf_friend_id = models.CharField(max_length=255, null=False, default=False)
    uf_favorite = models.BooleanField(null=False, default="False")

    class Meta:
        db_table = 'user_friend'
        verbose_name = '친구목록'
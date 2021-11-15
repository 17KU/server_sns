from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=64, unique=True, null=False, default=False)
    user_pw = models.CharField(max_length=256, null=False, default=False)
    user_name = models.CharField(max_length=400, null=False, default=False)

    class Meta :
        db_table = 'user'
        verbose_name = '유저 테이블'
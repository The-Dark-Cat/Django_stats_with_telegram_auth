import time
from hashlib import md5

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    telegram_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    keitaro_username = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def get_unique_token(self):
        # возвращает уникальный токен для пользователя, состоящий из хеша полей модели и времени создания токена
        return md5((str(self.telegram_id) + self.first_name + self.last_name + self.username + str(time.time())).encode('utf-8')).hexdigest()

    class Meta:
        unique_together = (('username', ),)
        index_together = (('first_name', 'last_name'),)


class TempToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class UserWhitelist(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    keitaro_username = models.CharField(max_length=50)







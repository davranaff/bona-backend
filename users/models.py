from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    town = models.CharField(verbose_name='town', max_length=60, blank=True, null=True)
    street = models.CharField(verbose_name='street', max_length=100, blank=True, null=True)
    house = models.CharField(verbose_name='house', max_length=100, blank=True, null=True)
    telephone = models.CharField(verbose_name='telephone number', unique=True, max_length=30, blank=False, null=False)
    created_at = models.DateTimeField(verbose_name="created time", auto_created=True, auto_now_add=True, blank=True,
                                      null=True)

    custom_email = models.ForeignKey('Email', verbose_name='User email', on_delete=models.PROTECT,
                                     related_name='user_email', null=True)
    confirmed = models.BooleanField(verbose_name='Confirmed', default=False)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        db_table = "users"


class Email(models.Model):
    created_at = models.DateTimeField(verbose_name="created time", auto_created=True, auto_now_add=True, blank=True,
                                      null=True)
    email = models.EmailField(verbose_name="email", blank=True, unique=True, null=True)
    code = models.IntegerField(verbose_name="email code", blank=True, null=True)

    def __str__(self):
        return self.email

# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Пользователь',
        null=True,
    )
    phone_number = models.CharField('Номер телефона', max_length=20, blank=True)
    address = models.CharField('Адрес', max_length=250, blank=True)
    postal_code = models.CharField('Индекс', max_length=20, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    country = models.CharField('Страна', max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'
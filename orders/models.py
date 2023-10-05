# -*- coding: utf-8 -*-

from django.db import models
from listings.models import Product
from django.conf import settings
from django.urls import reverse

ORDER_STATUS = [
    ('Created', 'Created'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Ready for pickup', 'Ready for pickup'),
    ('Completed', 'Completed')
]

TRANSPORT_CHOICES = [
    ('Courier delivery', 'Courier delivery'),
    ('Recipient pickup', 'Recipient pickup')
]

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        blank=True,
        null=True
    )
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Почта', )
    telephone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=250)
    postal_code = models.CharField('Индекс', max_length=20)
    city = models.CharField('Город', max_length=100)
    country = models.CharField('Страна', max_length=100)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обнавлен', auto_now=True)
    status = models.CharField('Стиатус', max_length=20, choices=ORDER_STATUS,
                              default='Создан')
    note = models.TextField(blank=True)
    transport = models.CharField('Достака', max_length=20, choices=TRANSPORT_CHOICES)
    transport_cost = models.DecimalField('Стоимось доставки', max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order #{self.id}'

    def get_absolute_url(self):
        return reverse(
            'orders:order_detail',
            args=[self.id]
        )

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost += self.transport_cost
        return total_cost

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', )


    class Meta:
        verbose_name = 'Список заказов'
        verbose_name_plural = 'Список заказов'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

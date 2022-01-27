# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from listings.models import Product
from .forms import CartAddProductForm
from decimal import Decimal


def get_cart(request):
    # функция где создается сессия
    cart = request.session.get(settings.CART_ID)
    if not cart:
        cart = request.session[settings.CART_ID] = {}
    return cart


def cart_add(request, product_id):
    cart = get_cart(request)# сессию заносим в переменную
    product = get_object_or_404(Product, id=product_id)
    product_id = str(product.id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        if product_id not in cart:# если нет айди в карзине
            cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if request.POST.get('overwrite_qty'): # из шаблона overwrite_qty прилетает value True
            cart[product_id]['quantity'] = cd['quantity']  # заносим в сессию
        else:
            cart[product_id]['quantity'] += cd['quantity']  # если другие значния, накапливаем корзину в сессию из данных в форме

        request.session.modified = True  # Затем мы помечаем сессию как
        # modified (измененную) для сохранения в Django.

        return redirect('cart:cart_detail')

def cart_detail(request):
    cart = get_cart(request)# Начнем с извлечения корзины из сессии.
    product_ids = cart.keys() # извлекая ключи корзины.
    products = Product.objects.filter(id__in=product_ids) # мы получаем список наших товаров в корзине
    temp_cart = cart.copy() # создаем копию нашей корзины

    for product in products: # выполняем итерацию по объектам наших товаров в корзине
        cart_item = temp_cart[str(product.id)] # для каждого
        cart_item['product'] = product # объекта добавляем экземпляр товара и стоимость
        cart_item['total_price'] = (Decimal(cart_item['price']) #  вычисляем общую стоимость
                                    * cart_item['quantity'])
        cart_item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': cart_item['quantity']
            #     Мы создаем экземпляр CartAddProductForm для каждого элемента в
            # корзине, чтобы пользователь мог обновлять количество. И создаем
            # форму с текущим количеством товара присутствующим в корзине.
        })

    cart_total_price = sum(Decimal(item['price']) * item['quantity'] #  вычисляем общую стоимость
                           for item in temp_cart.values())

    return render(
        request,
        'detail.html',
        {
            'cart': temp_cart.values(),
            'cart_total_price': cart_total_price
        })


def cart_remove(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]

        request.session.modified = True

        return redirect('cart:cart_detail')

def cart_clear(request):
    del request.session[settings.CART_ID]
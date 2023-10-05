# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order, Product
from .forms import OrderCreateForm
from cart.views import get_cart, cart_clear
from decimal import Decimal
from django.conf import settings
import stripe
from .tasks import order_created
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from django.http import HttpResponse

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)

    return render(
        request,
        'order_detail.html',
        {'order': order}
    )


def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    # generate pdf
    html = render_to_string('pdf.html', {'order': order})
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=stylesheets)

    return response

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from oauth2_provider.decorators import protected_resource
# @protected_resource()
import logging
from django.http import HttpResponse
logger = logging.getLogger(__name__)

import requests
def order_create(request, claims='0'):
    logger.debug("Test!!1002 ")
    logger.debug(f"claims-51-create, '{claims}'")
    # logger.debug(f"oidc_states-order_create-52, '{request.session.get['oidc_states_myOIDCstate']}'")
    test_var = request
    request_user = request.user
    logger.debug(f"order_views_request_GET_2702:: '{test_var}'")
    logger.debug(f"order_views_request_user2702:: '{request_user}'")
    # test_var = {'code': ['1a88624d0d74472a8b7c98a65119f310']}
    # tmp_token = test_var['id_token'][0]
    # logger.debug(f"test_varo:: '{tmp_token}'")

    # url = 'http://finesauces.pp.ua/'
    # data = {"param1": "value1", "param2": "value2"}
    # headers = {'Content-Type': 'application/json'}
    # # response = requests.get(url, data=data, headers=headers)
    # response = requests.get(url, data=data, headers=headers)
    # logger.debug('response11', response)
    # criipto_url = "https://inesauces-test.criipto.id/oauth2/authorize?" \
    #               "scope=openid&" \
    #               "client_id=urn:finesauces:identifier:8933&" \
    #               "redirect_uri=http://finesauces.pp.ua/orders/create/&" \
    #               "response_type=code&" \
    #               "response_mode=query&" \
    #               "nonce=ecnon-ab6d698f-324b-417a-ab67-289f6700fecc&prompt=login&" \
    #               "acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low"

    criipto_url = "https://inesauces-test.criipto.id/oauth2/authorize?" \
                  "response_type=id_token&" \
                  "client_id=urn:finesauces:identifier:8933&" \
                  "redirect_uri=http://finesauces.pp.ua/authcriipto/index_view_two/&" \
                  "acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low&" \
                  "scope=openid&" \
                  "state=etats&" \

    #####150222
    # criipto_url = "https://inesauces-test.criipto.id/oauth2/authorize?" \
    #               "response_type=code&response_mode=query&" \
    #               "client_id=urn:finesauces:identifier:8933&" \
    #               "redirect_uri=http://finesauces.pp.ua/orders/create/&" \
    #               "acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low&scope=openid&" \
    #               "state=etats&" \
    #               "code_challenge=pn0RVb2z6MAWlffU0puaJeIR63gShh6OF5yz2LZCr-4&" \
    #               "nonce=ecnon-ab6d698f-324b-417a-ab67-289f6700fecc&" \
    #               "code_challenge_method=S256"

    cart = get_cart(request)
    cart_qty = sum(item['quantity'] for item in cart.values())
    transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            cf = order_form.cleaned_data
            transport = cf['transport']

            if transport == 'Recipient pickup':
                transport_cost = 0

            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.transport_cost = Decimal(transport_cost)
            order.save()

            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                cart_item = cart[str(product.id)]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=cart_item['price'],
                    quantity=cart_item['quantity']
                )

            customer = stripe.Customer.create(
                email=cf['email'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=int(order.get_total_cost() * 100),
                currency='usd',
                description=order
            )

            cart_clear(request)

            order_created.delay(order.id)

            return render(
                request,
                'order_created.html',
                {'order': order}
            )
    # elif request.GET.get('q'):
    #     if request.user.is_authenticated:
    #         order.user = request.user
    #         order.transport_cost = Decimal(transport_cost)
    #         order.save()
    #
    #         product_ids = cart.keys()
    #         products = Product.objects.filter(id__in=product_ids)
    #
    #         for product in products:
    #             cart_item = cart[str(product.id)]
    #             OrderItem.objects.create(
    #                 order=order,
    #                 product=product,
    #                 price=cart_item['price'],
    #                 quantity=cart_item['quantity']
    #             )
    #
    #         customer = stripe.Customer.create(
    #             email=cf['email'],
    #             source=request.POST['stripeToken']
    #         )
    #     else:
    #         logger.debug(f"order_views_request_user_153:: '{'2'}'")
    #     return HttpResponse("<h1>Hello</h1>")
    else:
        order_form = OrderCreateForm()
        if request.user.is_authenticated:
        #     initial_data = {
        #         'first_name': request.user.first_name,
        #         'last_name': request.user.last_name,
        #         'email': request.user.email,
        #         'telephone': request.user.profile.phone_number,
        #         'address': request.user.profile.address,
        #         'postal_code': request.user.profile.postal_code,
        #         'city': request.user.profile.city,
        #         'country': request.user.profile.country,
        #     }
        #     order_form = OrderCreateForm(initial=initial_data)
        # else:
            initial_data = {
                'first_name': 'first_name',
                'last_name': 'last_name',
                'email': 'email@email.com',
                'telephone': '11235436574685',
                'address': 'Jltccf',
                'postal_code': '123445',
                'city': 'esyrytiuto',
                'country': 'Yjhdt',
            }
            order_form = OrderCreateForm(initial=initial_data)

    return render(
        request,
        'order_create_bac_oidc.html',
        {
            'cart': cart,
            'order_form': order_form,
            'transport_cost': transport_cost,
            'criipto_url': criipto_url
        }
    )

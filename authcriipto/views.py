import io
import os

from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from kombu.asynchronous.http import curl

from oauth2_provider.views.generic import ProtectedResourceView
import requests


import logging
from django.http import HttpResponse, response
from urllib3.util import url

logger = logging.getLogger(__name__)

import requests

from django.template.loader import render_to_string
from django.template import Template, Context

def index_view(request):
    logger.debug('request-33', request)
    r = requests.get("https://inesauces-test.criipto.id/oauth2/authorize?scope=openid&client_id=urn:finesauces:identifier:8933&redirect_uri=http://finesauces.pp.ua/orders/create/&response_type=code&response_mode=query&nonce=ecnon-4259be2d-f12b-45b1-a626-0c609c8b51dd&prompt=login&acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low")
    response = requests.get(r.url)
    logger.debug('response', response)
    # logger.debug('response', r.status_code)
    # logger.debug('response', r.headers)
    logger.debug(f"r.url36 :: '{r.url}'")
    # logger.debug('r.content', r.url)
    # logger.debug('response', r.text)
    # response = requests.get(url, params=params)

# curl -X POST 'https://inesauces-test.criipto.id/oauth2/authorize/' \
    #     -H 'scope: openid' \
    #     -H 'client_id=urn:finesauces:identifier:8933' \
    #     -H 'redirect_uri=http://finesauces.pp.ua/orders/create/' \
    #     -H 'response_type=code&response_mode=query&nonce=ecnon-4259be2d-f12b-45b1-a626-0c609c8b51dd&prompt=login&' \
    #     -H 'acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low' \


# curl -X POST \
#     https://your_domain/o/token/ \
#     -H 'Content-Type: application/x-www-form-urlencoded' \
#     -d 'grant_type=password&client_id=your_client_id&client_secret=your_client_secret&username=your_username&password=your_password'
    logger.debug(f"r.urlresponse :: '{response}'")
    bytes_stream = io.BytesIO(r.content)
    bytes_stream_tw = r.content.decode()
    logger.debug(f"bytes_stream :: '{bytes_stream.getvalue()}'")
    bytes_stream.close()

    logger.debug(f"bytes_stream_tw :: '{bytes_stream_tw}'")
    # file = open("indexx.html","w")
    # file.write(bytes_stream_tw)
    # file.close()
    # return HttpResponse("https://inesauces-test.criipto.id/oauth2/authorize?scope=openid&client_id=urn:finesauces:identifier:8933&redirect_uri=http://finesauces.pp.ua/orders/create/&response_type=code&response_mode=query&nonce=ecnon-4259be2d-f12b-45b1-a626-0c609c8b51dd&prompt=login&acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low"
    # return HttpResponse(curl, "https://inesauces-test.criipto.id/oauth2/authorize?scope=openid&client_id=urn:finesauces:identifier:8933&redirect_uri=http://finesauces.pp.ua/orders/create/&response_type=code&response_mode=query&nonce=ecnon-4259be2d-f12b-45b1-a626-0c609c8b51dd&prompt=login&acr_values=urn:grn:authn:no:bankid urn:grn:authn:no:bankid:substantial urn:grn:authn:dk:mitid:low"
    #                     )





    # def my_view(request):
    arbitrary_string_as_template =f"{bytes_stream_tw}"

    # arbitrary_string_as_template = """
    #     <form action="" method="POST">
    #     {% csrf_token %}
    #     <label for="">Username</label>
    #     <input type="text" name="username">
    #     <label for="">Password</label>
    #     <input type="password" name="password">
    #     <button type="submit">
    #         submit
    #     </button>
    #     </form>
    # """
    template = Template(arbitrary_string_as_template)
    context = RequestContext(request)
    # test_var = {'code': ['1a88624d0d74472a8b7c98a65119f310']}
    # logger.debug(f"test_var:: '{test_var['code'][0]}'")
    # my_token_code = test_var['code'][0]

    return HttpResponse(template.render(context))

    # template = Template('Hello {{name}}.')
    # context = Context(dict(name='World'))
    # rendered: str = template.render(context)
    # template = Template('{% now "d M Y" %}, Login as {{ user }}')
    # rendered_template = template.render(RequestContext(request))

    # ren = render_to_string('indexx.html', {'bytes_stream_tw': bytes_stream_tw},) #следующие элементы сохранить в кеше
    # return HttpResponse(ren)


    # return render(request, 'index.html')
    # return render(request, 'indexx.html')
    # return render(request, 'indexx.html')
    # return render(request, r)
    # teytu = os.fsencode(r.content)
    # return render(request, teytu)

def index_view_two(request):
    test_var = request.session
    # test_var = request.GET.get('id_token', None)
    logger.debug(f"request_var--113:: '{test_var}'")
    # return render(request, 'indexx.html', {'test_var': test_var})

    # return HttpResponse("<h1>Hello</h1>", content_type="text/plain", charset="utf-8")
    return redirect('http://finesauces.pp.ua/orders/create?q=1', foo='bar')

# @login_required
# def home_view(request):
#     return render(request, 'home.html')
#
# class ApiEndpoint(ProtectedResourceView):
#     def get(self, request, *args, **kwargs):
#         # return some data
#         return render(request, 'api-endpoint.html')

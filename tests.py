from django.test import TestCase

# Create your tests here.
# -*- coding: utf-8 -*-
import random
import string

import requests

string  # = 'f7666b4f7eee4e65b0fb954253cc6ce3'
import base64
import hashlib

#code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits))# for range(random.randint(43 )))
code_verifier = base64.urlsafe_b64encode('f7666b4f7eee4e65b0fb954253cc6ce3'.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

print(code_verifier)
print(code_challenge)
# bytes_stream = io.BytesIO(r.content)
bytes_stream_tw = code_verifier.decode()
print('bytes_stream_tw', bytes_stream_tw)
# bytes_stream_tw.close()


# curl -X POST \
# -H "Cache-Control: no-cache" \
# -H "Content-Type: application/x-www-form-urlencoded" \
r = requests.post(
    "http://finesauces.pp.ua/o/token/",
    data={
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        # "http://finesauces.pp.ua/o/token/"
        "client_id": "spNkszvPkwDtwKEmKxcenmbqD23Tsu1ecwi5ZxKc",
        "client_secret": "pbkdf2_sha256$216000$kUC0dGNFZg7g$O2qZUKckOp7eezBiE0EYoCPz+Ub6CKwcSry/7ub1CLI=",
        "code": "f7666b4f7eee4e65b0fb954253cc6ce3",
        "code_verifier": "Zjc2NjZiNGY3ZWVlNGU2NWIwZmI5NTQyNTNjYzZjZTM=",
        "redirect_uri": "http://finesauces.pp.ua/",
        "grant_type": "authorization_code",
        "scope": "read write",
    },
)
print(r.headers)
print(r.status_code)
print(r)


rr = requests.post(
    'http://127.0.0.1:8999/o/token/',
    data={
        'grant_type': 'password',
        'username': 'tinez99',
        'password': 'ovHCQPuxu2OeRTYz6H8LwA',
        'client_id': 'BRswr7zZAbICJvGnzgO7ve5A3dm6vJowQcCDDIye',
        'client_secret':'pbkdf2_sha256$390000$KibGZTgzhDJPtLsnMPj7et$Su1w30tSFV7LQ4nf9vRvYs5Z7gSWZWUugGKxArSv/+o=',
    },
)
print(rr.headers)
print(rr.status_code)
print(rr)



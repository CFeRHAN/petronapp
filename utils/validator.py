import requests
import json
from rest_framework.response import Response
from django.conf import settings


def uploader_validator(params):
    URL = settings.UPLOADER_URL
    req = requests.get(url = URL + params + '/')
    response = json.loads(req.text)
    if response['exists'] != 'true':
        return Response({'message':'your file aint uploaded yet'})
    else:
        pass
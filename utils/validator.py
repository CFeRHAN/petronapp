import requests, json, re
from rest_framework.response import Response
from django.conf import settings


def key_existance(list, key):
    return key in list and list[key]


def uploader_validator(params):
    URL = settings.UPLOADER_URL
    req = requests.get(url = URL + params + '/')
    response = json.loads(req.text)
    if response['exists'] != 'true':
        return Response({'message':'your file aint uploaded yet'})
    else:
        pass


def mobile_validator(mobile):
    # mobile_regex = "^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$"
    # mobile_regex_98 = "^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$"
    # if(re.search(mobile_regex, mobile)):
    #     true_mobile = '98' + mobile[1:]
    #     return true_mobile

    # elif(re.search(mobile_regex_98, mobile)):
    #     return mobile

    # else:
    #     return False

    valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for item in mobile:
        if item not in valid_chars:
            return False

    if (mobile[:3] != '989' or len(str(mobile)) != 12):
        true_mobile = '98' + mobile[1:]
        return true_mobile
    elif (mobile[0:3] == '989' or len(str(mobile)) ==12):
        return mobile


    



    
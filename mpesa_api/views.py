import json
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from mpesa_api.models import Mpesa
from .models import RobermsMpesa, TeuleMpesa
from sms.models import Group, Contact, TobentoTill, Customer
from rest_framework.response import Response
from django_daraja.mpesa.core import MpesaClient
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)

def get_mpesa_access_token():
    consumer_key = "JwvAC8cvoV659urQ9QLE9Eaks8yzAxX9"
    consumer_secret = "MJ6JrgVlWoYjapbD"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


def mpesa_express(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0724648426'
    amount = 10
    account_reference = 'rent'
    transaction_desc = 'Description'
    callback_url = 'https://endpint.roberms.com/roberms/mpesa_express/'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def express_push(request):
    phone = request.POST.get("phone_number")
    amount = request.POST.get("amount")
    if phone is None or amount is None:
        return Response({'error': 'Please provide both phone number and Amount'}, status=HTTP_400_BAD_REQUEST)
    

    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = phone
    amount = amount
    account_reference = 'rent'
    transaction_desc = 'Description'
    callback_url = 'https://endpint.roberms.com/roberms/mpesa_express/'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)



    

    if not user:
        context = {
            'error': 'Invalid Credentials',
        }
        return Response(context, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    context = {
        'token': token.key,
    }
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
def register_urls(request):
    access_token = get_mpesa_access_token()
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://roberms.co.ke/api/v1/c2b/confirmation",
               "ValidationURL": "https://roberms.co.ke/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def validation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    context = {
        "ResultCode": 1,
        "ResultDesc": "Failed",
        "ThirdPartyTransID": 0
    }
    url = 'https://rentalkenya.com/api/company_admin/v1/validation'
    body = {
        # "TransactionType": mpesa_payment['TransactionType'],
        # "TransID": mpesa_payment['TransID'],
        # "TransTime": mpesa_payment['TransTime'],
        # "TransAmount": mpesa_payment['TransAmount'],
        # "BusinessShortCode": mpesa_payment['BusinessShortCode'],
        "BillRefNumber": mpesa_payment["BillRefNumber"],
        # "InvoiceNumber": mpesa_payment['InvoiceNumber'],
        # "OrgAccountBalance": mpesa_payment['OrgAccountBalance'],
        # "ThirdPartyTransID": mpesa_payment['ThirdPartyTransID'],
        # "MSISDN": mpesa_payment['MSISDN'],
        # "FirstName": mpesa_payment['FirstName'],
        # "MiddleName": mpesa_payment['MiddleName'],
        # "LastName": mpesa_payment['LastName']
        }
    response = requests.post(url=url, json=body)
    return JsonResponse(json.loads(response.text))


@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    Mpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="admin@roberms.com",
        type=mpesa_payment['TransactionType'],
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']
    )

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    url = 'https://rentalkenya.com/api/company_admin/v1/confirmation'
    body = {
        "TransactionType": mpesa_payment["TransactionType"],
        "TransID": mpesa_payment["TransID"],
        # "TransTime": mpesa_payment["TransTime"],
        "TransAmount": mpesa_payment["TransAmount"],
        # "BusinessShortCode": mpesa_payment["BusinessShortCode"],
        "BillRefNumber": mpesa_payment["BillRefNumber"],
        # "InvoiceNumber": mpesa_payment["InvoiceNumber"],
        # "OrgAccountBalance": mpesa_payment["OrgAccountBalance"],
        # "ThirdPartyTransID": mpesa_payment["ThirdPartyTransID"],
        "MSISDN": mpesa_payment["MSISDN"],
        "FirstName": mpesa_payment["FirstName"],
        # "MiddleName": mpesa_payment["MiddleName"],
        "LastName": mpesa_payment['MiddleName'],
        }
    response = requests.post(url=url, json=body)
    return JsonResponse(dict(context))


def get_mpesa_access_token2():
    consumer_key = "LfVqGr8L714Tc9d6xW4Cf3R2OqigcVy7"
    consumer_secret = "MJmQvcH1GjTyALsW"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token

def get_mpesa_access_token_teule():
    consumer_key = "2GjwP28mfGkQBfhU3qrLQdsjqFKAY1eS"
    consumer_secret = "Vq1klmJRyjXLzA0u"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token

@csrf_exempt
def register_urls_teule(request):
    access_token = get_mpesa_access_token_teule()
    print ("here are tthhe acess tokens")
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "4057701",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://sba.roberms.com/api/v1/c2b/teule/confirmation",
               "ValidationURL": "https://sba.roberms.com/api/v1/c2b/142374/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def register_urls_4112827(request):
    access_token = get_mpesa_access_token2()
    
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "4112827",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://sba.roberms.com/api/v1/c2b/teule/confirmation",
               "ValidationURL": "https://sba.roberms.com/api/v1/c2b/142374/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def validation2(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Completed"
    }

    return JsonResponse(dict(context))

from django.core.files import File
@csrf_exempt

def confirmation2(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    f_name=mpesa_payment['FirstName']
    descr=mpesa_payment['TransID']
    phone=mpesa_payment['MSISDN']
    f = open('/var/log/thiss_err.log', 'w')
    testfile = File(f)
    testfile.write(mpesa_body)
    testfile.close
    f.close
    RobermsMpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['FirstName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="roberms@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']

        
    )

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted 1"
    }
    return JsonResponse(dict(context))

@csrf_exempt

def confirmation_teule(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    TeuleMpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['FirstName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="teule@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']

        
    )

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted 1"
    }
    return JsonResponse(dict(context))

def tobento_get_mpesa_access_token2():
    consumer_key = "p0FnFcdjpAsOeb3uqZ8ypegHaSnWIdA9"
    consumer_secret = "myb1ki4MOeGBFAgp"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


@csrf_exempt
def tobento_register_urls(request):
    access_token = tobento_get_mpesa_access_token2()
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "917137",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://roberms.co.ke/api/v1/c2b/tobento/196192/confirmation",
               "ValidationURL": "https://roberms.co.ke/api/v1/c2b/tobento/196192/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def tobento_validation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    logging.debug(f"Tobento Validation {mpesa_payment}")
    context = {
        "ResultCode": 0,
        "ResultDesc": "Completed"
    }

    return JsonResponse(dict(context))


@csrf_exempt
def tobento_confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    logging.debug(f"Mpesa response {mpesa_payment}")
    Mpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="tobento@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        customer_id=Customer.objects.filter(user_ptr_id=117).first().id,
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']
    )

    for till in TobentoTill.objects.all():
        if str(till.store_number) == mpesa_payment['BusinessShortCode']:
            group = Group.objects.filter(name__contains=str(till.till_number)).first()
            if group is not None:
                if Contact.objects.filter(group=group, phone_number=mpesa_payment['MSISDN']).count() < 1:
                    Contact.objects.create(
                        group=group,
                        email="tobento@roberms.com",
                        phone_number=mpesa_payment['MSISDN'],
                        name=f"{mpesa_payment['FirstName']} {mpesa_payment['MiddleName']}"
                    )
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


# AVERY LOUNGE
def avery_get_mpesa_access_token2():
    consumer_key = ""
    consumer_secret = ""
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


@csrf_exempt
def avery_register_urls(request):
    access_token = tobento_get_mpesa_access_token2()
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://roberms.co.ke/api/v1/c2b/avery/196192/confirmation",
               "ValidationURL": "https://roberms.co.ke/api/v1/c2b/avery/196192/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def avery_validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Completed"
    }

    return JsonResponse(dict(context))


@csrf_exempt
def avery_confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    Mpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="avery@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        customer_id=Customer.objects.filter(user_ptr_id=204).first().id,
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']
    )
    till_number = ''
    if till_number == mpesa_payment['BusinessShortCode']:
        group = Group.objects.filter(name__contains=str(till_number)).first()
        if group is not None:
            if Contact.objects.filter(group=group, phone_number=mpesa_payment['MSISDN']).count() < 1:
                Contact.objects.create(
                    group=group,
                    email="avery@roberms.com",
                    phone_number=mpesa_payment['MSISDN'],
                    name=f"{mpesa_payment['FirstName']} {mpesa_payment['MiddleName']}"
                )
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


def mayanet_get_mpesa_access_token2():
    consumer_key = "GWqAeQHCChXSv70Ty7OYSYZMGZRwIV73"
    consumer_secret = "0LFpQj6tMuefWZXT"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


@csrf_exempt
def mayanet_register_urls(request):
    pass_key = "e9a59cbc0ca05ecf88ac75bb9bf4137ef9d67d7963d103c611d17f08452c5dfb"
    access_token = mayanet_get_mpesa_access_token2()
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "533382",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://roberms.co.ke/api/v1/c2b/mayanet/533382/confirmation",
               "ValidationURL": "https://roberms.co.ke/api/v1/c2b/mayanet/533382/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def mayanet_validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Completed"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def mayanet_confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    Mpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="mayanet@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        customer_id=Customer.objects.filter(user_ptr_id=58).first().id,
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']
    )

    till_number = mpesa_payment['BusinessShortCode']
    group = Group.objects.filter(name__contains=str(till_number)).first()
    if group is not None:
        if Contact.objects.filter(group=group, phone_number=mpesa_payment['MSISDN']).count() < 1:
            Contact.objects.create(
                group=group,
                email="mayanet@roberms.com",
                phone_number=mpesa_payment['MSISDN'],
                name=f"{mpesa_payment['FirstName']} {mpesa_payment['MiddleName']}"
            )
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


def mayanet2_get_mpesa_access_token2():
    consumer_key = "AhoKXp4YlH7ujFCD7UPAY8GR1aGIVrO7"
    consumer_secret = "jOEeHkFmAStUvfrx"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


@csrf_exempt
def mayanet2_register_urls(request):
    pass_key = "5257923f3781f63136dd5e0ea316937ef8acc36ec90e1c033ecd188695c7c5ac"
    access_token = mayanet2_get_mpesa_access_token2()
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "4027033",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://roberms.co.ke/api/v1/c2b/mayanet/4027033/confirmation",
               "ValidationURL": "https://roberms.co.ke/api/v1/c2b/mayanet/4027033/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def mayanet2_validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Completed"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def mayanet2_confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    Mpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="mayanet2@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        customer_id=Customer.objects.filter(user_ptr_id=58).first().id,
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']
    )

    till_number = mpesa_payment['BusinessShortCode']
    group = Group.objects.filter(name__contains=str(till_number)).first()
    if group is not None:
        if Contact.objects.filter(group=group, phone_number=mpesa_payment['MSISDN']).count() < 1:
            Contact.objects.create(
                group=group,
                email="mayanet@roberms.com",
                phone_number=mpesa_payment['MSISDN'],
                name=f"{mpesa_payment['FirstName']} {mpesa_payment['MiddleName']}"
            )
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


def tntsky_mpesa_access_token():
    consumer_key = "AflXgIAUBc66yuhQcyYb21ccyAaiM0PC"
    consumer_secret = "l84boGSVJv8jxvBk"
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


@csrf_exempt
def tntsky_register_urls(request):
    pass_key = "c1e778a2ab40b46bfb1d40d83518f2585fc4c75f47c12508bf2e05a91e575c67"
    access_token = tntsky_mpesa_access_token()
    print(access_token)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": "4047479",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://roberms.co.ke/api/v1/c2b/tntsky/4047479/confirmation",
               "ValidationURL": "https://roberms.co.ke/api/v1/c2b/tntsky/4047479/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def tntsky_validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Completed"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def tntsky_confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    Mpesa.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        email="tandt@roberms.com",
        type=mpesa_payment['TransactionType'],
        account_number=mpesa_payment['BusinessShortCode'],
        # customer_id=Customer.objects.filter(user_ptr_id=58).first().id,
        created_at=timezone.now(),
        organization_balance=mpesa_payment['OrgAccountBalance']
    )

    till_number = mpesa_payment['BusinessShortCode']
    group = Group.objects.filter(name__contains=str(till_number)).first()
    if group is not None:
        if Contact.objects.filter(group=group, phone_number=mpesa_payment['MSISDN']).count() < 1:
            Contact.objects.create(
                group=group,
                email="mayanet@roberms.com",
                phone_number=mpesa_payment['MSISDN'],
                name=f"{mpesa_payment['FirstName']} {mpesa_payment['MiddleName']}"
            )
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


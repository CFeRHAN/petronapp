import random
import string

from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from freight.models import Freight
from freight.serializers import *

from orders.models import *
from orders.serializers import *
from orders.views import create_paperwork

from utils.validator import uploader_validator, key_existance, mobile_validator
from utils.senders import send_password

from flow_manager.views import flow_manager


@swagger_auto_schema(methods=['POST'], request_body=CreateFreightProfileSerializer)
@api_view(['GET', 'POST'])
def profile(request, format=None):
    """endpoint that allows user to create Producer profile"""

    user = request.user
    mobile = user.mobile
    

    if request.method == 'GET':
        user = Freight.objects.get(mobile=mobile)
        serializer = CreateFreightProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user.delete()
        freight = Freight.objects.create(mobile=mobile)

        if user.role == "0":
            serializer = CreateFreightProfileSerializer(freight, data=request.data)
            if serializer.is_valid():
                
                if key_existance(serializer.validated_data, 'profile_picture_file'):
                    if not serializer.validated_data['profile_picture_file'] == '-':
                        params = serializer.validated_data['profile_picture_file']
                        uploader_validator(params)
                    

                if key_existance(serializer.validated_data, 'license_file'):
                    if not serializer.validated_data['license_file'] == '-':
                        params = serializer.validated_data['license_file']
                        uploader_validator(params)                
                
                if key_existance(serializer.validated_data, 'company_doc_file'):
                    if not serializer.validated_data['company_doc_file'] == '-':
                        params = serializer.validated_data['company_doc_file']
                        uploader_validator(params)
                
                if key_existance(serializer.validated_data, 'permission_file'):
                    if not serializer.validated_data['permission_file'] == '-':
                        params = serializer.validated_data['permission_file']
                        uploader_validator(params)
                
                if key_existance(serializer.validated_data, 'agent_phone'):
                    mobile = serializer.validated_data['agent_phone']
                    agent_mobile = mobile_validator(mobile)
                
                if key_existance(serializer.validated_data, 'mobile'):
                    mobile = serializer.validated_data['mobile']
                    mobile = mobile_validator(mobile)
                    
    
                serializer.validated_data['role'] = '2'
                serializer.validated_data['mobile'] = mobile
                serializer.validated_data['agent_phone'] = agent_mobile
                serializer.save()

                if 'password' not in serializer.validated_data:
                    
                    rand = random.SystemRandom()
                    digits = rand.choices(string.digits, k=6)
                    password =  ''.join(digits)
                    
                else:
                    password = serializer.validated_data['password']
                    
                    
                freight.set_password(password)  
                freight.role = '2'
                data = {'password': password, 'recipient':user.mobile}
                send_password(data)
                freight.permission_file = serializer.validated_data['permission_file']
                freight.save()


                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'you already have a profile'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'there is something wrong'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def orders(request, format=None):
    """endpoint that returns a list of orders for freight companies"""

    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        
        orders = Order.objects.all()
        my_offers = Offer.objects.filter(freight=user).values_list('order_id', flat=True)
        accepted_offers = Offer.objects.filter(freight_acception=True).values_list('order_id', flat=True)
        available_orders = orders.exclude(pk__in=my_offers)
        available_orders = available_orders.exclude(pk__in=accepted_offers)
        serializer = OrderSerializer(available_orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def accepted_offers(request, format=None):

    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        offers = Offer.objects.filter(freight=user, freight_acception=True, orderer_acception=True)
        offer_id = offers.values_list('id', flat=True)
        accepted_offers = []
        for id in offer_id:
            flow = flow_manager(id, user)
            offer = Offer.objects.get(id=id)
            accepted_offers.append({'offer':OfferSerializer(offer).data, 'flow':flow})

        return Response(accepted_offers , status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def nonaccepted_offers(request, format=None):
    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "2":
        offers = Offer.objects.filter(freight=user, freight_acception=False)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_detail(request, order_pk, format=None):
    """endpoint that returns details of an order for the Express company"""

    user = request.user

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "2":
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def offers(request, format=None):
    """endpoint that returns a list of offers that is made by the Freight company"""

    user = request.user

    if request.method == 'GET':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "2":
            offers = Offer.objects.filter(freight=user.id)
            serializer = OfferSerializer(offers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def offer_detail(request, offer_pk, format=None):
    """endpoint that returns details about an offer made by the Freight company and let them update it"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role == "2":
            serializer = OfferSerializer(offer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=CreateOfferReqSerializer)
@api_view(['POST'])
def create_offer(request, order_pk, format=None):
    """endpoint that allows a Freight company to create an offer for specified order"""

    user = request.user

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        serializer = CreateOfferSerializer(data=request.data)
        req_serializer = CreateOfferReqSerializer(data=request.data)

        if req_serializer.is_valid() and serializer.is_valid():

            if key_existance(req_serializer.validated_data, 'deal_draft_file'):
                    if not req_serializer.validated_data['deal_draft_file'] == '-':
                        params = req_serializer.validated_data['deal_draft_file']
                        uploader_validator(params)

            
            serializer.validated_data['freight'] = user
            serializer.validated_data['order'] = order
            serializer.validated_data['deal_draft'] = create_paperwork(req_serializer.validated_data['deal_draft_file'])
            if Offer.objects.filter(freight=user, order=order.id).exists():
                return Response({'message': 'you already have an offer for this order'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UpdateOfferSerializer)
@api_view(['POST'])
def update_offer(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to update an offer for specified order"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        offered_prices = []
        last_offered_price = offer.price
        offered_prices.append(last_offered_price)
        serializer = UpdateOfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            freight = User.objects.get(id=user.id)
            order = Order.objects.get(pk=order_pk)
            
            serializer.validated_data['freight'] = freight
            serializer.validated_data['order'] = order
            serializer.validated_data['seen'] = False
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def offer_confirmation(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to confirm an already given offer"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        order = Order.objects.get(pk=order_pk)
        offers = Offer.objects.filter(order=order_pk)
        for offer in offers:
            if offer.freight_acception == True:
                return Response({'message': 'an other Freight company has already registered for this order'}, status=status.HTTP_400_BAD_REQUEST)
        offer.freight_acception = True
        offer.order = order
        offer.save()
        serializer = OfferSerializer(offer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_order_number(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to view order_number"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == '0':
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == '2':
        serializer = ViewOrderNumberSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['order_number_seen_status'] = 'True'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(methods=['POST'], request_body=UploadDriversInfoSerializer)
@api_view(['POST'])
def upload_drivers_info(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to upload drivers info"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "2":
        serializer = UploadDriversInfoSerializer(data=request.data)
        if serializer.is_valid():

            bill_file = serializer.validated_data['bill_file']
            drivers_info = PaperWork(bill_file=bill_file)
            drivers_info.save()
            offer.drivers_info = drivers_info
            offer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(methods=['POST'], request_body=UploadDemurrageBillSerializer)
@api_view(['POST'])
def upload_demurrage_bill(request, order_pk, offer_pk):
    """endpoint that allows a Freight company to upload a demurrage bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        serializer = UploadDemurrageBillSerializer(data=request.data)
        if serializer.is_valid():

            bill_file = serializer.validated_data['bill_file']
            price = serializer.validated_data['price']

            demurrage_bill = Payment(bill_file=bill_file, price=price)
            demurrage_bill.save()
            offer.demurrage = demurrage_bill
            offer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmInventoryBillSerializer)
@api_view(['PUT'])
def confirm_inventory_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to confirm a received inventory bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        inventory = offer.inventory
        serializer = ConfirmInventoryBillSerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfrimPrepaymentBillSerializer)
@api_view(['PUT'])
def confrim_prepayment_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to confirm or reject a prepayment"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        prepayment = offer.prepayment
        serializer = ConfrimPrepaymentBillSerializer(prepayment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadPrepaymentReceiptSerializer)
@api_view(['POST'])
def upload_prepayment_reciept(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to upload prepeyment confirmation receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        prepayment = offer.prepayment
        serializer = UploadPrepaymentReceiptSerializer(prepayment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_load_information(request, order_pk, offer_pk, format=None):
    """endpoint that retrieves Loading Information for an Order"""
    
    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        load_info = offer.load_info
        print(load_info)
        serializer = ViewLoadInfoSerializer(load_info)
        print(serializer.data)
        load_info.status = True
        load_info.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(methods=['POST'], request_body=UploadLadingBillSerializer)
@api_view(['POST'])
def upload_lading_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows A Freight company to upload lading bill for an offer."""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        
        serializer = UploadLadingBillSerializer(data=request.data)
        if serializer.is_valid():
            
            bill_file = serializer.validated_data['bill_file']
            lading_bill = PaperWork(bill_file=bill_file)
            lading_bill.save()
            offer.lading_bill = lading_bill
            offer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadInventoryReceiptSerializer)
@api_view(['POST'])
def upload_inventory_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows the Freight company to upload Inventory Payment Reciept"""

    user = request.user


    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        serializer = UploadInventoryReceiptSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(methods=['PUT'], request_body=ConfirmDemurrageReceiptSerializer)
@api_view(['PUT'])
def confirm_demurrage_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to confirm a paid demurrage receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        demurrage = offer.demurrage
        serializer = ConfirmDemurrageReceiptSerializer(demurrage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(methods=['PUT'], request_body=ConfirmBijakBillSerializer)
@api_view(['PUT'])
def confirm_bijak_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows a Freight company to confirm the given Bijak"""

    user = request.user
    
    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        bijak = offer.bijak
        serializer = ConfirmBijakBillSerializer(bijak, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def order_completion_approval(request, order_pk, offer_pk, format=None):
    """endpoint that allows Freight company to approve that an order cycle is finished"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        order = offer.order
        order.freight_completion_date=timezone.datetime.now()
        order.save()
        return Response({'success':'Order Completion Approved'}, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadSecondDestinationBillSerializer)
@api_view(['POST'])
def upload_second_destination_cost(request, order_pk, offer_pk, format=None):
    """endpoint that allows Freight company to upload Second Destination Bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        serializer = UploadSecondDestinationBillSerializer(data=request.data)

        if serializer.is_valid():
            bill_file = serializer.validated_data['bill_file']
            price = serializer.validated_data['price']

            cost = Payment(bill_file=bill_file, price=price)
            cost.save()
            offer.second_destination_cost = cost
            offer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(methods=['PUT'], request_body=ConfirmFinalPaymentReceiptSerializer)
@api_view(['PUT'])
def confirm_final_payment_receipt(request, order_pk, offer_pk, format=None):
    """endpoint in which Freight company confirms that has received all the money"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "2":
        final_payment = offer.final_payment
        serializer = ConfirmFinalPaymentReceiptSerializer(final_payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)




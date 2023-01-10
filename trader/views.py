import random
import string

from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from trader.serializers import *
from trader.models import Trader

from orders.models import *
from orders.serializers import *

from utils.validator import uploader_validator, key_existance, mobile_validator
from utils.senders import send_password

from flow_manager.views import flow_manager


@swagger_auto_schema(methods=['POST'], request_body=CreateTraderProfileSerializer)
@api_view(['GET', 'POST'])
def profile(request, format=None):
    """endpoint that allows user to create Trader profile"""

    user = request.user
    mobile = user.mobile
    


    if request.method == 'GET':
        user = Trader.objects.get(mobile=mobile)
        serializer = CreateTraderProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user.delete()
        trader = Trader.objects.create(mobile=mobile)
        if user.role == "0":
            serializer = CreateTraderProfileSerializer(trader, data=request.data)
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
                
                if key_existance(serializer.validated_data, 'agent_phone'):
                    mobile = serializer.validated_data['agent_phone']
                    agent_mobile = mobile_validator(mobile)
                
                if key_existance(serializer.validated_data, 'mobile'):
                    mobile = serializer.validated_data['mobile']
                    mobile = mobile_validator(mobile)
                                            
                serializer.validated_data['mobile'] = mobile
                serializer.validated_data['agent_phone'] = agent_mobile
                serializer.save()

                if 'password' not in serializer.validated_data:
                    
                    rand = random.SystemRandom()
                    digits = rand.choices(string.digits, k=6)
                    password =  ''.join(digits)
                    
                else:
                    password = serializer.validated_data['password']
                    
                    
                trader.set_password(password)  
                trader.role = '1'
                trader.mobile = mobile
                data = {'password':password, 'recipient':user.mobile}
                send_password(data)
                trader.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(user.role, user.id)
            return Response({'message':'you already have a profile'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'there is something wrong'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=CreateOrderSerializer)
@api_view(['GET', 'POST'])
def orders(request, format=None):
    """Lists all orders for express and user's order for trader"""
    user = request.user

    if request.method == 'GET':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "1":
            orders = Order.objects.filter(orderer=user.id)
            y = []
            for order in orders:
                offers = Offer.objects.filter(order=order)
                offer_count = len(offers)
                serializer = OrderSerializer(order)
                x = {'order':serializer.data, 'offer_count':offer_count}
                y.append(x)
            return Response(y, status=status.HTTP_200_OK)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if user.role == "1":
            serializer = CreateOrderSerializer(data=request.data)
            if serializer.is_valid():


                if key_existance(serializer.validated_data, 'order_number_file'):
                    if not serializer.validated_data['order_number_file'] == '-':
                        params = serializer.validated_data['order_number_file']
                        uploader_validator(params)

                if key_existance(serializer.validated_data, 'proforma_file'):
                    if not serializer.validated_data['proforma_file'] == '-':
                        params = serializer.validated_data['proforma_file']
                        uploader_validator(params)


                serializer.validated_data['orderer_id'] = user.id
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'Method not allowed!'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=OrderSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, order_pk, format=None):
    """endpoint that retrieves updates and deletes an order"""
    user = request.user
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "1":
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "1":
            serializer = OrderSerializer(order, data=request.data)  # needs a change in serializer perhaps
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "1":
            offer = Offer.objects.get(order__id=order_pk)
            if offer:
                return Response({"Failed": "You cant delete an order with an offer related"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                order.delete()
                return Response({"Success": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def offers(request, order_pk, format=None):
    """endpoint that retrieves received offers for an order"""

    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        offers = Offer.objects.filter(order=order_pk)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def offer_detail(request, order_pk, offer_pk):

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order_id=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        offer_serializer = OfferSerializer(offer).data
        order_serializer = OrderSerializer(order).data

        return Response({'offer_items':offer_serializer, 'order_items':order_serializer}, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def offer_acception(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to select an offer for the giver order"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == '0':
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if user.role == '1':
        offers = Offer.objects.filter(order=order_pk)
        for offer in offers:
            if offer.freight_acception == True:
                return Response({'message': 'you already accepted an offer for this order'}, status=status.HTTP_400_BAD_REQUEST)
        offer.orderer_acception = True
        offer.save()
        serializer = OfferAcceptionSerializer(offer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def approved_offers(request, format=None):
    """endpoint that returns a list of Producer's orders that have been approved"""

    user = request.user
    # user = User.objects.get(id=22)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":        
        offers = Offer.objects.filter(order__orderer=user, orderer_acception=True, freight_acception=True)
        offer_id = offers.values_list('id', flat=True)
        approved_offers = []
        for id in offer_id:
            flow = flow_manager(id, user)
            offer = Offer.objects.get(id=id)
            approved_offers.append({'offer':OfferSerializer(offer).data, 'flow':flow})
        
        return Response(approved_offers, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_deal_draft(request, order_pk, offer_pk, format=None):
    """endpoints that shows the deal draft to Trader"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.deal_draft
        draft = PaperWork.objects.get(pk=x)
        serializer = ViewDealDraftSerializer(draft)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ViewOrderNumberSerializer)
@api_view(['PUT'])
def send_order_number(request, order_pk, offer_pk):
    """endpoints that allows Trader to send the order number to Freight"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        order = Order.objects.get(pk=order_pk)

        order_number = order.order_number_file
        offer.order_number_file = order_number
        offer.save()

        serializer = ViewOrderNumberSerializer(offer, data=request.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadPrepaymentBillSerializer)
@api_view(['PUT'])
def upload_prepayment_bill(request, order_pk, offer_pk, format=None):

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        x = offer.prepayment
        prepayment = Payment.objects.get(pk=x)
        serializer = UploadPrepaymentBillSerializer(prepayment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['PUT'], request_body=ConfirmPrepaymentReceiptSerializer)
@api_view(['PUT'])
def confirm_prepayment_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows the trader to confirm the given receipt for paid prepayment"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.prepayment
        receipt = Payment.objects.get(pk=x)
        serializer = ConfirmPrepaymentReceiptSerializer(receipt, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['receipt_status'] == False:
                x = offer.prepayment
                prepayment_receipt = Payment.objects.get(pk=x)
                prepayment_receipt.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmLadingBillSerializer)
@api_view(['PUT'])
def confirm_lading_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to view the Lading bill for an order"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        x = offer.lading_bill
        lading = PaperWork.objects.get(pk=x)
        serializer = ConfirmLadingBillSerializer(lading, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['bill_status'] == False:
                lading.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmInventoryBillSerializer)
@api_view(['PUT'])
def confirm_inventory_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to confirm Inventory Bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.inventory
        inventory = Payment.objects.get(pk=x)
        serializer = ConfirmInventoryBillSerializer(inventory, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['bill_status'] == False:
                inventory.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmDemurrageBillSerializer)
@api_view(['PUT'])
def confirm_demurrage_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to confirm Inventory Bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.inventory
        demurrage = Payment.objects.get(pk=x)
        serializer = ConfirmDemurrageBillSerializer(demurrage, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['bill_status'] == False:
                demurrage.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadInventoryReceiptSerializer)
@api_view(['PUT'])
def upload_inventory_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to upload a inventory receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        x = offer.demurrage_bill
        inventory = Payment.objects.get(pk=x)
        serializer = UploadInventoryReceiptSerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadDemurrageReceiptSerializer)
@api_view(['PUT'])
def upload_demurrage_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to upload a demurrage receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        x = offer.demurrage_bill
        demurrage = Payment.objects.get(pk=x)
        serializer = UploadDemurrageReceiptSerializer(demurrage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def order_completion_approval(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader company to approve that an order cycle is finished"""    
    
    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "1":
        order = Order.objects.get(pk=order_pk)
        order.orderer_completion_date = timezone.now()
        order.save()
        return Response({'success':'True'}, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=DefineSecondDestinationSerializer)
@api_view(['PUT'])
def define_second_destination(request, order_pk, offer_pk, format=None):
    """endpoint that allows Trader to define a second destination for an order"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.order
        order = Order.objects.get(pk=x)
        serializer = DefineSecondDestinationSerializer(order, data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmSecondDestinationBillSerializer)
@api_view(['PUT'])
def confirm_second_destination_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to confrim the bill for Second Destination"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.second_destination_cost
        cost = Payment.objects.get(pk=x)
        serializer = ConfirmSecondDestinationBillSerializer(cost, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['bill_status'] == False:
                cost.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadSecondDestinationReceiptSerializer)
@api_view(['PUT'])
def upload_second_destination_cost_receipt(request, order_pk, offer_pk, format=None):

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == '0':
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == '1':

        serializer = UploadSecondDestinationReceiptSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'400-This endpoint does not belong to your role'}, status=status.HTTP_400_BAD_REQUEST)
    


@swagger_auto_schema(methods=['PUT'], request_body=UploadFinalPaymentReceipt)
@api_view(['PUT'])
def upload_final_payment_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows the Trader to upload the Final Payment Receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "1":
        x = offer.final_payment
        final_payment = Payment.objects.get(pk=x)
        serializer = UploadFinalPaymentReceipt(final_payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
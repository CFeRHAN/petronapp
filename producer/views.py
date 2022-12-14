import random
import string

from django.utils import timezone
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from producer.serializers import *
from producer.models import Producer

from orders.models import *
from orders.serializers import *
from orders.views import offer_counter

from utils.validator import uploader_validator, key_existance, mobile_validator
from utils.senders import send_password

from flow_manager.views import flow_manager


@swagger_auto_schema(methods=['POST'], request_body=CreateProducerProfileSerializer)
@api_view(['GET', 'POST'])
def profile(request, format=None):
    """endpoint that allows user to create Producer Profile"""
    
    user = request.user
    mobile = user.mobile
    

    if request.method == 'GET':
        user = Producer.objects.get(mobile=mobile)
        serializer = CreateProducerProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user.delete() 
        producer = Producer.objects.create(mobile=mobile)
        if user.role == "0":
            serializer = CreateProducerProfileSerializer(producer, data=request.data)
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
                    agent_mobile = serializer.validated_data['agent_phone']
                    agent_mobile = mobile_validator(agent_mobile)
                
                if key_existance(serializer.validated_data, 'mobile'):
                    mobile = serializer.validated_data['mobile']
                    mobile = mobile_validator(mobile)

                serializer.validated_data['role'] = '3'
                serializer.validated_data['mobile'] = mobile
                serializer.validated_data['agent_phone'] = agent_mobile
                serializer.save()

                if 'password' not in serializer.validated_data:
                    
                    rand = random.SystemRandom()
                    digits = rand.choices(string.digits, k=6)
                    password =  ''.join(digits)
                    
                else:
                    password = serializer.validated_data['password']
                    
                    
                producer.set_password(password)  
                producer.role = '3'
                data = {'password': password, 'recipient':user.mobile}
                send_password(data)
                producer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'you already have a profile'}, status=status.HTTP_400_BAD_REQUEST)
            
    else:
        return Response({'message':'there is something wrong'}, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(methods=['POST'], request_body=ProducerOrderSerializer)
@api_view(['GET', 'POST'])
def orders(request, format=None):
    """Creates new order with POST / Returns a list of orders with GET"""
    
    user = request.user
    producer = User.objects.get(pk=user.id)

    if request.method == 'GET':
        
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "3":
            orders = Order.objects.filter(orderer=user.id)
            y = []
            for order in orders:
                offers = Offer.objects.filter(order=order)
                offer_count = len(offers)
                serializer = ProducerOrderSerializer(order)
                x = {'order':serializer.data, 'offer_count':offer_count}
                y.append(x)
            return Response(y, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "3":
            serializer = ProducerCreateOrderSerializer(data=request.data)
            if serializer.is_valid():

                if key_existance(serializer.validated_data, 'order_number_file'):
                    if not serializer.validated_data['order_number_file'] == '-':
                        params = serializer.validated_data['order_number_file']
                        uploader_validator(params)

                if key_existance(serializer.validated_data, 'proforma_file'):
                    if not serializer.validated_data['proforma_file'] == '-':
                        params = serializer.validated_data['proforma_file']
                        uploader_validator(params)


                serializer.validated_data['orderer'] = user
                serializer.validated_data['producer'] = producer
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def recieved_orders(request, format=None):
    """Creates new order with POST / Returns a list of orders with GET"""
    
    user = request.user
    producer = User.objects.get(pk=user.id)

    if request.method == 'GET':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "3":
            orders = Order.objects.filter(producer=user.id)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_detail(request, order_pk):
    """endpoint that returns an order detail of a Producer"""

    user = request.user

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if user.role == "3":
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def offers(request, order_pk, format=None):
    """endpoint that returns a list of offers, recieved for a single Order"""

    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "3":
        offers = Offer.objects.filter(order=order_pk)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def offer_detail(request, order_pk, offer_pk, format=None):
    """endpoint that returns details about an offer"""

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

    elif user.role == "3":
        offer_serializer = OfferSerializer(offer).data
        order_serializer = OrderSerializer(order).data
        

        return Response({'offer_items':offer_serializer, 'order_items':order_serializer}, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['PUT'])
def offer_acception(request, order_pk, offer_pk, format=None):
    """endpoint that allows producer to accept an offer"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
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

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        offers = Offer.objects.filter(Q(order__orderer=user) | Q(order__producer=user), orderer_acception=True, freight_acception=True)    
        offer_id = offers.values_list("id", flat=True)
        approved_offers = []
        for id in offer_id:
            flow = flow_manager(id, user)
            offer = Offer.objects.get(id=id)
            approved_offers.append({'offer':OfferSerializer(offer).data, 'flow':flow})
            
        return Response(approved_offers, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadOrderNumberSerializer)
@api_view(['PUT'])
def upload_order_number(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to upload the Order Number"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        order = Order.objects.get(pk=order_pk)

        serializer = UploadOrderNumberSerializer(order, data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_drivers_info(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to view drivers info"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "3":
        serializer = ViewDriversInfoSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['status'] = 'True'
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadInventoryBillSerializer)
@api_view(['POST'])
def upload_invetory_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to view drivers info"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "3":

        serializer = UploadInventoryBillSerializer(data=request.data)
        if serializer.is_valid():
            bill_file = serializer.validated_data['bill_file']
            price = serializer.validated_data['price']
            inventory = Payment(bill_file=bill_file, price=price)
            inventory.save()
            offer.inventory = inventory
            offer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_demurrage_bill(request, order_pk, offer_pk, format =None):
    """endpoint that allows producer to view demurrage bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        serializer = ViewDemurrageBillSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadPaymentBillSerializer)
@api_view(['PUT'])
def upload_prepayment_bill(request, order_pk, offer_pk):
    """endpoint that allows producer to view the prepayment confirmation receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
        x = offer.prepayment
        prepayment = Payment.objects.get(pk=x)
        serializer = UploadPaymentBillSerializer(prepayment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(methods=['PUT'], request_body=ConfirmPrepaymentRecieptSerializer)
@api_view(['PUT'])
def confirm_prepayment_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows producer to view and confirm the approval of the paid Pre-Payment"""
    
    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
        x = offer.prepayment
        prepayment = Payment.objects.get(pk=x)
        serializer = ConfirmPrepaymentRecieptSerializer(prepayment, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['receipt_status'] == False:
                prepayment.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadLoadInfoBillSerializer)
@api_view(['POST'])
def upload_load_information(request, order_pk, offer_pk, format=None):
    """endpoint that allows producer to upload the load information file"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":

        serializer = UploadLoadInfoBillSerializer(data=request.data)

        if serializer.is_valid():

            bill_file = serializer.validated_data['bill_file']
            load_info = PaperWork(bill_file=bill_file)
            load_info.save()
            offer.load_info = load_info
            offer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadInvoicePackingBillSerializer)
@api_view(['PUT'])
def upload_invoice_packing_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows producer to upload invoice packing bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
        x = offer.invoice_packing
        invoice_packing = PaperWork.objects.get(pk=x)
        serializer = UploadInvoicePackingBillSerializer(invoice_packing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmLadingBillSerializer)
@api_view(['PUT'])
def confirm_lading_bill(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to confirm lading bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
        x = offer.lading_bill
        lading = PaperWork.objects.get(pk=x)
        serializer = ConfirmLadingBillSerializer(lading, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['status'] == False:
                lading.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=ConfirmInventoryReceiptSerializer)
@api_view(['PUT'])
def confrim_inventory_reciept(request, order_pk, offer_pk, format=None):
    """endpoint that allows producer to confirm a paid inventory receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
        x = offer.inventory
        inventory = Payment.objects.get(pk=x)
        serializer = ConfirmInventoryReceiptSerializer(inventory, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['receipt_status'] == False:
                inventory.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=UploadDemurrageReceiptSerializer)
@api_view(['PUT'])
def upload_demurrage_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to upload a demurrage receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        x = offer.demurrage_bill
        demurrage = Payment.objects.get(pk=x)
        serializer = UploadDemurrageReceiptSerializer(demurrage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadBijakBillSerializer)
@api_view(['POST'])
def upload_bijak(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to upload a bijak"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":

        serializer = UploadBijakBillSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            bill_file = serializer.validated_data['bill_file']
            bijak = PaperWork(bill_file=bill_file)
            bijak.save()
            offer.bijak = bijak
            offer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT'], request_body=DefineSecondDestinationSerializer)
@api_view(['PUT'])
def define_second_destination(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer to define a second destination for an order"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
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
    
    elif user.role == "3":
        x = offer.second_destination_cost
        cost = Payment.objects.get(pk=x)
        serializer = ConfirmSecondDestinationBillSerializer(cost, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['bill_status'] == False:
                cost.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def order_completion_approval(request, order_pk, offer_pk, format=None):
    """endpoint that allows Producer company to approve that an order cycle is finished"""    
    
    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        order = Order.objects.get(pk=order_pk)
        order.orderer_completion_date = timezone.datetime.now()
        order.save()
        return Response({'success':'True'}, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UploadFinalPaymentReceipt)
@api_view(['POST'])
def upload_final_payment_receipt(request, order_pk, offer_pk, format=None):
    """endpoint that allows the Trader to upload the Final Payment Receipt"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif user.role == "3":
        serializer = UploadFinalPaymentReceipt(data=request.data)

        if serializer.is_valid():

            receipt_file = serializer.validated_data['receipt_file']
            final_payment = Payment(receipt_file=receipt_file)
            final_payment.save()
            offer.final_payment = final_payment
            offer.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_all_producers(request, format=None):
    user = request.user
    if user.role != '0' :
        producers = User.objects.filter(role='3')
        serializer = ProducerSerializer(producers, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

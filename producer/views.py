from django.utils import timezone

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



@swagger_auto_schema(methods=['PUT'], request_body=CreateProducerProfileSerializer)
@api_view(['GET', 'PUT'])
def create_profile(request, pk, format = None):
    """endpoint that allows user to create Producer Profile"""
    
    user = request.user
    
    producer = User.objects.get(mobile=user.mobile)

    if request.method == 'GET':
        serializer = CreateProducerProfileSerializer(producer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        
        if user.role == "0":
            serializer = CreateProducerProfileSerializer(producer, data=request.data)
            if serializer.is_valid():
                serializer.validated_data['role'] = '3'
                serializer.save()
                password = user.mobile[8:]
                producer.set_password(password)
                producer.role = '3'
                producer.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_200_OK)
        else:
            return Response({'message':'you already have a profile'}, status=status.HTTP_400_BAD_REQUEST)
            
    else:
        return Response({'message':'there is something wrong'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def create_profile2(request, pk, format = None):
    """endpoint that allows user to create a Producer profile"""
    
    user = request.user
    producer = User.objects.get(mobile=user.mobile)
    

    if request.method == 'GET':
        serializer = CreateProducerProfileSerializer(producer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        producer = Producer.objects.update(mobile=user.mobile)
        serializer = CreateProducerProfileSerializer(producer, data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data['role'] = '3'
            serializer.save()

            password = user.mobile[8:]
            user.set_password(password)
            user.role = '3'
            user.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
            
    else:
        return Response({'message':'there is something wrong'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def orders(request, format=None):
    """Creates new order with POST / Returns a list of orders with GET"""
    
    user = request.user
    producer = User.objects.get(pk=user.id)

    if request.method == 'GET':
        print(user)
        print(f'this is role:::',user.role)
        
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "3":
            orders = Order.objects.filter(orderer=user.id)
            serializer = ProducerOrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "3":
            serializer = ProducerOrderSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.validated_data)
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
    producer = Producer.objects.get(pk=user.id)

    if request.method == 'GET':
        print(user.role)
        print(producer)
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
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def offer_detail(request,order_pk, offer_pk, format=None):
    """endpoint that returns details about an offer"""

    user = request.user

    offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    order = Order.objects.get(pk=order_pk)
    freight = Freight.objects.get(pk=offer.freight)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        offer_serializer = OfferSerializer(offer).data
        order_serializer = Order_OfferSerializer(order).data
        freight_serializer = Freight_OfferSerializer(freight).data

        return Response({'offer_items':offer_serializer, 
                         'order_items':order_serializer,
                         'freight_items':freight_serializer},
                          status=status.HTTP_200_OK)

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
        offer.orderer_acception = True
        offer.save()
        serializer = OfferAcceptionSerializer(offer)

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def approved_orders(request, format=None):
    """endpoint that returns a list of Producer's orders that have been approved"""

    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif user.role == "3":
        
        offers = Offer.objects.filter(order__orderer=user, orderer_acception=True, freight_acception=True)
        orders = []
        for offer in offers:
            order_id = offer.order.id
            a = Order.objects.get(id=order_id)
            orders.append(a)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        serializer = UploadOrderNumberSerializer(offer, data=request.data)
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
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
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
        x = offer.inventory
        inventory = Payment.objects.get(pk=x)
        serializer = UploadInventoryBillSerializer(offer, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
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


@api_view(['PUT'])
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
        x = offer.load_info
        load_info = PaperWork.objects.get(pk=x)
        serializer = UploadLoadInfoBillSerializer(load_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
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


@swagger_auto_schema(methods=['PUT'], request_body=UploadBijakBillSerializer)
@api_view(['PUT'])
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
        x = offer.bijak
        bijak = PaperWork.objects.get(pk=x)
        serializer = UploadBijakBillSerializer(bijak, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        serializer = OrderCompletionAprroveserializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def vieW_all_producers(request, format=None):
    user = request.user
    if user.role != '0' :
        producers = Producer.objects.all()
        serializer = ProducerSerializer(producers, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


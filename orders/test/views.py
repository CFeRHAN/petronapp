from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.api.serializers import *
from orders.models import *


# Trader ENDPOINTS

@swagger_auto_schema(methods=['POST'], request_body=OrderSerializer)
@api_view(['GET', 'POST'])
def trader_orders(request, format=None):
    """endpoint that returns a Trader's orders with GET and creates an order with POST"""

    user = request.user
    if request.method == 'GET':
        if user.role == "0":
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "1":
            orders = Order.objects.filter(orderer=user.id)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "1":
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def trader_order_detail(request, order_pk):
    """endpoint that returns an order detail of a Trader"""

    user = request.user
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "1":
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def trader_offers(request, order_pk, format=None):
    """endpoint that returns a list of offers, recieved for a single Order"""

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
def trader_offer_detail(request, order_pk, offer_pk):
    """endpoint that returns a single offer's detail, recieved for an order"""

    user = request.user
    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "1":
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def trader_approved_orders(request):
    """endpoint for returns a list of Trader's orders that have been approved"""

    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "1":
        offers = Offer.objects.filter(order__orderer=user, orderer_completion_date__isnull=False, freight_completion_date__isnull=False)
        print(offers)
        orders = []
        for offer in offers:
            order_id = offer.order.id
            a = Order.objects.get(id=order_id)
            orders.append(a)
        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def trader_approved_order_detail(request, order_pk, format=None):
    """endpoint that returns details about a single approved order"""

    user = request.user

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "1":
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadPaymentRecieptSerializer)
# @api_view(['PUT'])
# def trader_payment_reciept(request, offer_pk):
#     """endpoint that allows Trader to upload the Payment Reciept"""

#     user = request.user

#     try:
#         reciept = PaymentReceipt.objects.get(offer__express=user, offer__id=offer_pk)
#     except PaymentReceipt.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     elif user.role == "1":
#         serializer = UploadPaymentRecieptSerializer(reciept)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmLadingBillSerializer)
# @api_view(['PUT'])
# def trader_lading_bill(request, offer_pk):
#     """endpoint that allows Trader to confirm Lading Bill"""

#     user = request.user
#     try:
#         lading = Lading.objects.get(offer__express=user, offer__id=offer_pk)
#     except Lading.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         serializer = ConfirmLadingBillSerializer(lading, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadCheckoutBillSerializer)
# @api_view(['PUT'])
# def trader_checkout_bill(request, offer_pk, format=None):
#     """endpoint that allows Trader to upload Checkout Bill"""

#     user = request.user

#     try:
#         checkout = Checkout.objects.get(offer__express=user, offer__id=offer_pk)
#     except Checkout.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         serializer = UploadCheckoutBillSerializer(checkout, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)


# @api_view(['PUT'])
# def trader_approval(request, order_pk):
#     """endpoint that allows Trader to approve that an order cycle is finished"""

#     user = request.user

#     try:
#         order = Order.objects.get(pk=order_pk)
#     except Order.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
        
#         order.user_done_approval = 1
#         order.save()
#         return Response({"Success": "Your approval just submitted"}, status=status.HTTP_200_OK)

#     else:
#         return Response(status =status.HTTP_400_BAD_REQUEST)
    


# @api_view(['GET'])
# def offer_counter(request, order_pk):
#     """endpoint that counts offers recieved for an order"""

#     try:
#         offers = Offer.objects.filter(order=order_pk)
#     except Offer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     print(offers)
#     serializer = OfferCountSerializer(offers)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def approval_check(request, order_pk):
#     """endpoint that checks wether an order is approved"""

#     user = request.user


#     try:
#         order = Order.objects.get(pk=order_pk)
#     except Order.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1" or "2":
#         trader_approval = order.user_done_approval
#         express_approval = order.express_done_approval

#         if trader_approval & express_approval == True:
#             return Response({"Success":"This order is Done"}, status=status.HTTP_200_OK)
#         elif trader_approval == True and express_approval == False:
#             return Response({"Warning":"express doesnt confirm"}, status=status.HTTP_200_OK)
#         elif trader_approval == False and express_approval == True:
#             return Response({"Warning":"trader doesnt confirm"}, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# Express ENDPOINTS


@api_view(['GET'])
def express_orders(request, format=None):
    """endpoint that returns a list of orders for express company"""
    
    user = request.user

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "2":
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def express_order_detail(request, order_pk, format=None):
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


@swagger_auto_schema(methods=['POST'], request_body=OfferSerializer)
@api_view(['GET', 'POST'])
def express_offers(request, order_pk, format=None):
    """endpoint that returns a list of offers that is made by the Express company"""

    user = request.user

    if request.method == 'GET':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "2":
            offers = Offer.objects.filter(express=user.id)
            serializer = OfferSerializer(offers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        if user.role == "0":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.role == "2":
            serializer = CreateOfferSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

@swagger_auto_schema(methods=['PUT'], request_body=OfferSerializer)
@api_view(['PUT'])
def express_offer_detail(request, offer_pk, order_pk):
    """endpoint that returns details about an offer made by the Express company"""
    
    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
        price = offer.price
        print(price)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.role == "0":
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif user.role == "2":
        serializer = CreateOfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmPaymentReceiptSerializer)
# @api_view(['PUT'])
# def express_payment_reciept(request, offer_pk):
#     """endpoint that allows Express to confirm a payment receipt"""

#     user = request.user

#     try:
#         reciept = PaymentReceipt.objects.get(offer__express=user, offer__id=offer_pk)
#     except PaymentReceipt.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = ConfirmPaymentReceiptSerializer(reciept, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadLadingBillSerializer)
# @api_view(['PUT'])
# def express_lading_bill(request, offer_pk):
#     """endpoint that allows Express to upload a LadingBill"""

#     user = request.user

#     try:
#         lading = Lading.objects.get(offer__express=user, offer__id=offer_pk)
#     except Lading.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = UploadLadingBillSerializer(lading, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmCheckoutBillSerializer)
# @api_view(['PUT'])
# def express_checkout_bill(request, offer_pk):
#     """endpoint that allows Express to confrim the Checkout Bill"""

#     user = request.user

#     try:
#         checkout = Checkout.objects.get(offer__express=user, offer__id=offer_pk)
#     except Checkout.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = ConfirmCheckoutBillSerializer(checkout, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    

# @swagger_auto_schema(methods=['PUT'], request_body=UploadDriversInformationsSerializer)
# @api_view(['PUT'])
# def express_drivers_info(request, offer_pk):
#     """endpoint that allows Express to upload Drivers Informations"""
    
#     user = request.user

#     try:
#         driver_info = Drivers.objects.get(offer__express=user, offer__id=offer_pk)
#     except Drivers.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = UploadDriversInformationsSerializer(driver_info, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadDemurrageBillSerializer)
# @api_view(['PUT'])
# def express_demurrage_bill(request, offer_pk):
#     """endpoint that allows Express to upload Demurrage Bill"""

#     user = request.user

#     try:
#         bill = Demurrage.objects.get(offer__express=user, offer__id=offer_pk)
#     except Demurrage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = UploadDemurrageBillSerializer(bill, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmInventorySerializer)
# @api_view(['PUT'])
# def express_inventory_bill(request, offer_pk):
#     """endpoint that allows Express to confirm Inventory Bill"""
    
#     user = request.user

#     try:
#         inventory = Inventory.objects.get(offer__express=user, offer__id=offer_pk)
#     except Inventory.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = ConfirmInventorySerializer(inventory, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfrimInvoiceSerializer)
# @api_view(['PUT'])
# def express_invoice_bill(request, offer_pk):
#     """endpoint that allows Express to confirm an Invoice"""
    
#     user = request.user

#     try:
#         invoice = Invoice.objects.get(offer__express=user, offer__id=offer_pk)
#     except Invoice.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = ConfrimInvoiceSerializer(invoice, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadOtherPricesBillSerializer)
# @api_view(['PUT'])
# def express_other_bills(request, offer_pk):
#     """endpoint that allows Express to upload Other Prices Bill"""
    
#     user = request.user

#     try:
#         bill = Other.objects.get(offer__express=user, offer__id=offer_pk)
#     except Other.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = UploadOtherPricesBillSerializer(bill, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmCheckoutBillSerializer)
# @api_view(['PUT'])
# def express_checkout_bill(request, offer_pk):
#     """endpoint that allows Express to confirm Checkout Bill"""
    
#     user = request.user

#     try:
#         checkout = Checkout.objects.get(offer__express=user, offer__id=offer_pk)
#     except Checkout.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
#         serializer = ConfirmCheckoutBillSerializer(checkout, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def express_approval(request, order_pk):
#     """endpoint that allows Express to approve that an order cycle is finished"""

#     user = request.user

#     try:
#         order = Order.objects.get(pk=order_pk)
#     except Order.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "2":
        
#         order.express_done_approval = 1
#         order.save()
#         return Response({"Success": "Your approval just submitted!"}, status=status.HTTP_200_OK)

#     else:
#         return Response(status =status.HTTP_400_BAD_REQUEST)


# # # PETRO ENDPOINTS


# @api_view(['GET'])
# def petro_express(request):
#     """endpoint that returns a list of Expresses that are about to carry a product from the Petro company"""

#     user = request.user

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "3":
#         offers = Offer.objects.filter(order__petro_seller_co=user, orderer_acception=True, express_acception=True)
#         expresses=[]
#         for offer in offers:
#             express = offer.express
#             expresses.append(express)
#         serializer = PetroExpressSerializer(expresses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def petro_approved_orders(request):
#     """endpoint that returns a list of Petro orders that have been approved"""
    
#     user = request.user

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "3":
#         offers = Offer.objects.filter(order__petro_seller_co=user, orderer_acception=True, express_acception=True)
#         print(offers)
#         orders = []
#         for offer in offers:
#             order_id = offer.order.id
#             a = Order.objects.get(id=order_id)
#             orders.append(a)
#         serializer = OrderSerializer(orders, many=True)
        
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadOrderNumberSerializer)
# @api_view(['PUT'])
# def petro_order_number(request, order_pk, offer_pk):
#     """endpoint that allows Petro to upload OrderNumber"""

#     user = request.user

#     try:
#         order_number = OrderNumber.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except OrderNumber.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     elif user.role == "3":
#         serializer = UploadOrderNumberSerializer(order_number)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmDriversInformationSerializer)
# @api_view(['PUT'])
# def petro_drivers_info(request, order_pk, offer_pk):
#     """endpoint that allows Petro to confirm Drivers Informations"""
    
#     user = request.user
#     try:
#         drivers_information = Drivers.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Drivers.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "3":
#         serializer = ConfirmDriversInformationSerializer(drivers_information, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmDemurrageBillSerializer)
# @api_view(['PUT'])
# def petro_demurrage_bill(request, order_pk, offer_pk):
#     """endpoint that allows Petro to confirm Demurrage Bill"""
    
#     user = request.user

#     try:
#         demurrage = Demurrage.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Demurrage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "3":
#         serializer = ConfirmDemurrageBillSerializer(demurrage, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadDemurragePaymentReceipt)
# @api_view(['PUT'])
# def petro_demurrage_payment(request, offer_pk):
#     """endpoint that allows Petro to upload the payment receipt for the approved Demurrage Bill"""

#     user = request.user

#     try:
#         demurrage = Demurrage.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Demurrage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     elif user.role == "3":
#         serializer = UploadDemurragePaymentReceipt(demurrage)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadInventoryBillSerializer)
# @api_view(['PUT'])
# def petro_inventory_bill(request, offer_pk):
#     """endpoint that allows Petro to upload Inventory Bill"""
    
#     user = request.user

#     try:
#         inventory = Inventory.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Inventory.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     elif user.role == "3":
#         serializer = UploadInventoryBillSerializer(inventory)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmInventoryPaymentReceiptSerializer)
# @api_view(['PUT'])
# def petro_inventory_receipt(request, offer_pk):
#     """endpoint that allows Petro to confirm the payment receipt for Inventory Bill"""

#     user = request.user

#     try:
#         inventory = Inventory.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Inventory.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "3":
#         serializer = ConfirmInventoryPaymentReceiptSerializer(inventory, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadPackagingBillSerializer)
# @api_view(['PUT'])
# def petro_packaging_bill(request, offer_pk):
#     """endpoint that allows Petro to upload Packaging Bill"""

#     user = request.user

#     try:
#         packaging = Packaging.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Packaging.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     elif user.role == "3":
#         serializer = UploadPackagingBillSerializer(packaging)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=UploadInvoiceBillSerializer)
# @api_view(['PUT'])
# def petro_invoice_bill(request, offer_pk):
#     """Endpoint that allows Petro to upload the Invoice(bijack) Bill"""

#     user = request.user

#     try:
#         invoice = Invoice.objects.get(offer__order__petro_seller_co=user, offer__id=offer_pk)
#     except Invoice.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     elif user.role == "3":
#         serializer = UploadInvoiceBillSerializer(invoice)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)



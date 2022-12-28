from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.serializers import *
from orders.models import *


@api_view(['GET'])
def order_dynamic_filter(request, format=None):
    queryset = Order.objects.all()
    weight_query = request.GET.get('weight')
    deal_type_query = request.GET.get('deal_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    border_passage = request.GET.get('border_passage')

    if weight_query != '' and weight_query is not None:
        queryset = queryset.filter(weight=weight_query)

    elif start_date is not None and end_date is not None:
        queryset = queryset.filter(loading_date__gte=start_date, loading_date__lte=end_date)

    elif deal_type_query != '' and deal_type_query is not None:
        queryset = queryset.filter(deal_type=deal_type_query)

    elif border_passage is not None:
        queryset = queryset.filter(border_passage)


    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def process_checkout(request, order_pk, offer_pk, format=None):
    """endpoint that gives the checkout bill"""

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk, orderer=user)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    price = offer.price

    prepayment = offer.prepayment.price
    second_destination_cost = offer.second_destination_cost.price
    final_payment = (price - prepayment) + second_destination_cost

    context = {'prepayment': prepayment, 'second_destination_cost': second_destination_cost, 'final_payment': final_payment}

    serializer = CheckoutSerializer(context, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def seen_offer(request, offer_pk):
    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    offer.seen = True
    offer.save()
    return Response(status=status.HTTP_200_OK)



def offer_counter(order_pk):
    try:
        offer = Offer.objects.filter(order__id=order_pk)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OfferCountSerializer(offer)
    return Response(serializer.data, status=status.HTTP_200_OK)


def create_paperwork(deal_draft_file, date=None):
    if date == None:
        date = datetime.date.today()
    return PaperWork.objects.create(bill_file=deal_draft_file, upload_date=date)


def create_payment(file_id, date=None):
    if date == None:
        date = datetime.date.today()
    return Payment.objects.create(bill_file=file_id, payment_date=date)
    






# @swagger_auto_schema(methods=['POST'], request_body=OrderSerializer)
# @api_view(['GET', 'POST'])
# def orders(request, format=None):
#     """Lists all orders for express and user's order for trader"""
#     user = request.user

#     if request.method == 'GET':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             orders = Order.objects.filter(user=user.id)
#             serializer = OrderSerializer(orders, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "2":
#             orders = Order.objects.all()
#             serializer = OrderSerializer(orders, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "3":
#             pass
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'POST':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             serializer = OrderSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif user.role == "2":
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         elif user.role == "3":
#             pass
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=OrderSerializer)
# @api_view(['GET', 'PUT', 'DELETE'])
# def order_detail(request, order_pk, format=None):
#     user = request.user
#     try:
#         order = Order.objects.get(pk=order_pk)
#     except Order.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             serializer = OrderSerializer(order)
#             return Response(serializer.data)
#         elif user.role == "2":
#             serializer = OrderSerializer(order)
#             return Response(serializer.data)
#         elif user.role == "3":
#             pass
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'PUT':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             serializer = OrderSerializer(order, data=request.data)  # needs a change in serializer perhaps
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "2":
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif user.role == "3":
#             pass
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             offer = Offer.objects.get(order__id=order_pk)
#             if offer:
#                 return Response({"Failed": "You cant delete an order with an offer related"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 order.delete()
#                 return Response({"Success": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         elif request.method == "2":
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif request.method == "3":
#             pass
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['POST'], request_body=OfferSerializer)
# @api_view(['GET', 'POST'])
# def offers(request, order_pk, format=None):
#     user = request.user

#     if request.method == 'GET':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             offers = Offer.objects.filter(order=order_pk)
#             serializer = OfferSerializer(offers, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "2":
#             offers = Offer.objects.filter(express=user.id)
#             serializer = OfferSerializer(offers, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "3":
#             pass
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'POST':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif user.role == "2":
#             serializer = OfferSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         elif user.role == "3":
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=OfferSerializer)
# @api_view(['GET', 'PUT'])
# def offer_detail(request, offer_pk):
#     user = request.user
#     try:
#         offer = Offer.objects.get(pk=offer_pk)
#     except Offer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             serializer = OfferSerializer(offer)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "2":
#             serializer = OfferSerializer(offer)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif user.role == "3":
#             pass

#     if request.method == 'PUT':
#         if user.role == "0":
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif user.role == "1":
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif user.role == "2":
#             serializer = OfferSerializer(offer, data=request.data)
#             price1 = 0
#             if serializer.is_valid():
#                 price2 = serializers
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif user.role == "3":
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def approved_orders(request):
#     user = request.user

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         offers = Offer.objects.filter(order__user=user, trader_acception=True, express_acception=True)
#         orders = []
#         for offer in offers:
#             order_id = offer.order.id  # check this out
#             orders.append(Order.objects.filter(user=user, id=order_id))
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "2":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "3":
#         pass
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def approved_order_detail(request, order_pk):
#     user = request.user
#     try:
#         order = Order.objects.get(pk=order_pk)
#     except Order.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "2":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "3":
#         pass
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT'], request_body=ConfirmPaymentReceiptSerializer)
# @api_view(['PUT'])
# def payment_reciept(request, offer_pk):
#     user = request.user

#     try:
#         reciept = PaymentReceipt.objects.get(offer__express=user, offer__id=offer_pk)
#     except PaymentReceipt.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         serializer = UploadPaymentRecieptSerializer(reciept, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "2":
#         serializer = ConfirmPaymentReceiptSerializer(reciept, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#     elif user.role == "3":
#         pass


# @swagger_auto_schema(methods=['PUT'], request_body=UploadLadingBillSerializer)
# @api_view(['PUT'])
# def lading_bill(request, offer_pk):
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
#     elif user.role == "2":
#         serializer = UploadLadingBillSerializer(lading, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def checkout_bill(request, offer_pk):
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
#     elif user.role == "2":
#         serializer = ConfirmCheckoutBillSerializer(checkout, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def order_number(request, offer_pk):
#     pass


# @api_view(['PUT'])
# def drivers_info(request, offer_pk):
#     user = request.user

#     try:
#         driver_info = Drivers.objects.get(offer__express=user, offer__id=offer_pk)
#     except Drivers.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = DriversInformationsSerializer(driver_info, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass

#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def demurrage_bill(request, offer_pk):
#     user = request.user

#     try:
#         bill = Demurrage.objects.get(offer__express=user, offer__id=offer_pk)
#     except Demurrage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = DemurrageBillSerializer(bill, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass

#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def inventory_bill(request, offer_pk):
#     user = request.user
#     try:
#         inventory = Inventory.objects.get(offer__express=user, offer__id=offer_pk)
#     except Inventory.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = ConfirmInventorySerializer(inventory, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass

#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def invoice_bill(request, offer_pk):
#     user = request.user
#     try:
#         invoice = Invoice.objects.get(offer__express=user, offer__id=offer_pk)
#     except Invoice.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = ConfrimInvoiceSerializer(invoice, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass

#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def other_bills(request, offer_pk):
#     user = request.user

#     try:
#         bill = Other.objects.get(offer__express=user, offer__id=offer_pk)
#     except Other.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = UploadOtherPricesBillSerializer(bill, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass

#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def checkout_bill(request, offer_pk):
#     user = request.user
#     try:
#         checkout = Checkout.objects.get(offer__express=user, offer__id=offer_pk)
#     except Checkout.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if user.role == "0":
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     elif user.role == "1":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif user.role == "2":
#         serializer = ConfirmCheckoutBillSerializer(checkout, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif user.role == "3":
#         pass

#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)

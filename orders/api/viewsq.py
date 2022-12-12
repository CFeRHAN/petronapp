from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from orders.api.serializers import *
from orders.models import *
from trader.models import Trader

### TRADER ###

class TraderOrdersListView(generics.ListCreateAPIView):
    # API View that lists orders and creates one or more

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(trader=user.id)
    

    def perform_create(self, serializer):
        trader = Trader.objects.filter(user=self.request.user).first()
        serializer.save(trader=trader)


class TraderOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    # API view that shows details of an order

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(trader=user.id)


class OfferListView(generics.ListAPIView):
    # APIView that shows a list of offers made by express companies for specified order

    permission_classes = [IsAuthenticated]
    serializer_class = OfferSerializer

    def get_queryset(self):
        user = self.request.user
        id = self.request.GET.get('id')
        return Offer.objects.filter(order=id)


class OfferDetailView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfferSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Offer.objects.filter(id=id)


class AgreedOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(is_confirmed_by_express=True, trader=user.id)


class AgreedOrdersDetailView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Order.objects.filter(id=id, is_confirmed_by_express=True)


class UploadPaymentRecieptView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadPaymentRecieptSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return PaymentReciept.objects.filter(offer_id=id)


class ConfirmLadingBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmLadingBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Lading.objects.filter(offer_id=id)


class UploadCheckoutBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Checkout.objects.filter(offer_id=id)



class OfferCountView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfferCountSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Offer.objects.filter(order_id=id)


### Express ###


class OrderListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class CreateOfferView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CreateOfferSerializer
    # queryset = Offer.objects.all()
    
    def get_queryset(self):
        id = self.request.GET.get('id')
        return Offer.objects.filter(order_id=id)


class OfferDetailUpdate(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CreateOfferSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Offer.objects.filter(express=user.id)


class OrderNumberView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewOrderNumberSerializer
    

    def get_queryset(self):
        id = self.request.GET.get('id')
        return OrderNumber.objects.filter(offer=id)


class UploadDriversInformationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DriversInformationsSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Drivers.objects.filter(offer_id=id)



class UploadDemurrageBill(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DemurrageBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Demurrage.objects.filter(offer_id=id)


class ConfirmInventoryBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmInventorySerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Inventory.objects.filter(offer_id=id)


class PackagingBillView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackagingBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Packaging.objects.filter(offer_id=id)


class UploadLadingBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadLadingBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Lading.objects.filter(offer_id=id)



class ConfirmInvoiceBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfrimInvoiceSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Invoice.objects.filter(offer_id=id)



class UploadOtherPricesBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadOtherPricesBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Other.objects.filter(offer_id=id)


class ConfirmCheckoutBillView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmCheckoutBillSerializer

    def get_queryset(self):
        id = self.request.GET.get('id')
        return Checkout.objects.filter(offer_id=id)
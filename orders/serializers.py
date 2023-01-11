from dataclasses import fields
from rest_framework import serializers

from orders.models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
        read_only_fields = ['orderer', 'orderer_completion_date', 'freight_completion_date', 'ordering_date']


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['orderer', 'orderer_completion_date', 'freight_completion_date', 'ordering_date']


class ProducerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        depth = 1
        fields = '__all__'
        read_only_fields = ['orderer', 'orderer_completion_date', 'freight_completion_date', 'ordering_date', 'producer']


class ProducerCreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['orderer', 'orderer_completion_date', 'freight_completion_date', 'ordering_date', 'producer']


class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['price', 'deal_draft', 'prepayment_percentage']
        depth = 1


class UpdateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['price', 'prepayment_percentage']


class CreateOfferReqSerializer(serializers.Serializer):
    price = serializers.FloatField()
    prepayment_percentage = serializers.IntegerField()
    deal_draft_file = serializers.CharField(max_length=35)



class OfferSerializer(serializers.ModelSerializer):
    prepayment_amount = serializers.SerializerMethodField(source='offer.get_prepayment_amount')

    class Meta:
        model = Offer
        fields = ['id', 'freight', 'price', 'prepayment_percentage', 'deal_draft', 'prepayment_amount', 'seen', 'order', 'freight_acception', 'orderer_acception']
        read_only_fields = ['prepayment_amount']
        depth = 2


    def get_prepayment_amount(request, self):
        """PrePayment Amount"""
        prepay = self.get_prepayment_amount()
        return prepay


class Order_OfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['product', 'weight', 'vehicle_type', 'loading_date']


class Freight_OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freight
        fields = ['about', 'company_name', 'url', 'company_phone', 'email']


class OfferDetailSerializer(serializers.ModelSerializer):
    order_items = Order_OfferSerializer(many=False, read_only=True)
    freights_items = Freight_OfferSerializer(many=True, read_only=True)
    class Meta:
        model = Offer
        fields = ['freights_items', 'price', 'prepayment_percentage', 'deal_draft', 'order_items']


# class ViewOrderNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Offer
#         fields = '__all__'
#         # fields = ['order_number', 'order_number_file']
#         # depth = 1
#         # read_only_fields = ['offer']


class OfferAcceptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['orderer_acception']
        

class ViewDriversInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['drivers_info', 'status']


class UploadInventoryBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'price']


class ViewDemurrageBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['demurrage']
        depth = 1


class UploadPaymentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['bill_file', 'bill_status', 'bill_rejection_reasons']


class ConfirmPrepaymentRecieptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['bill_file', 'price', 'payment_date']



class ConfirmPrepaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_file', 'receipt_status','receipt_rejection_reasons']
        read_only_fields = ['receipt_file']


class UploadLoadInfoBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_file']


class UploadInvoicePackingBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        exclude = ['status','rejection_reasons']


class ConfirmLadingBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['status','rejection_reasons']
        read_only_fields = ['bill_file']


class ConfirmInventoryReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_status', 'receipt_rejection_reasons', 'receipt_file']
        read_only_fields = ['receipt_file']


class UploadDemurrageReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_file']
        read_only_fields = ['bill_file']


class UploadBijakBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_file']


class DefineSecondDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['second_destination']



class ConfirmSecondDestinationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_status','bill_rejection_reasons','bill_file']
        read_only_fields = ['bill_file']


class UploadSecondDestinationReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_file', 'bill_file']
        read_only_fields = ['bill_file']



class OrdererCompletionAprroveserializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderer_completion_date']


class FreightCompletionAprroveserializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['freight_completion_date']


class ViewOrderNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['order_number', 'order_number_file', 'order_number_seen_status']


class UploadDriversInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_file']


class UploadDemurrageBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'price']


class ConfirmInventoryBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'bill_status','bill_rejection_reasons']
        read_only_fields = ['bill_file']


class ConfirmDemurrageBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'bill_status','bill_rejection_reasons']
        read_only_fields = ['bill_file']


class ConfrimPrepaymentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_status','bill_rejection_reasons', 'bill_file']
        read_only_fields = ['bill_file']


class ViewLoadInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = '__all__'
        # depth = 1


class UploadLadingBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_file']


class UploadInventoryReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_file', 'bill_file']
        read_only_fields = ['bill_file']


class ConfirmDemurrageReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_status', 'receipt_rejection_reasons']
        read_only_fields = ['bill_file']


class ConfirmBijakBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['status', 'rejection_reasons']
        read_only_fields = ['bill_file']


class UploadSecondDestinationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'price']


class ConfirmFinalPaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_status', 'receipt_rejection_reasons']
        read_only_fields = ['bill_file']


class OfferSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['orderer_acception']


class UploadPrepaymentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'price']


class UploadPrepaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_file']


class ViewDealDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = '__all__'
        depth = 1
        


class UploadFinalPaymentReceipt(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_file', 'receipt_file']
        read_only_fields = ['bill_file']


class UploadOrderNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order_number', 'order_number_file']


class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['price']


class OfferCountSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['number', 'order']

    def get_number(request, self):
        order = Offer.get_order()
        qs = Offer.objects.filter(order=order)
        number = qs.count()
        return number



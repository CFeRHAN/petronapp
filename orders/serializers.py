from dataclasses import fields
from rest_framework import serializers

from orders.models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['orderer', 'orderer_completion_date', 'freight_completion_date', 'ordering_date']


class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['price', 'deal_draft', 'prepayment_percentage']


class OfferSerializer(serializers.ModelSerializer):
    prepayment_amount = serializers.SerializerMethodField(source='offer.get_prepayment_amount')

    class Meta:
        model = Offer
        fields = ['id', 'freight', 'price', 'prepayment_percentage', 'deal_draft', 'prepayment_amount']
        read_only_fields = ['prepayment_amount']


    def get_prepayment_amount (request, self):
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


class ViewOrderNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['order_number']
        depth = 1
        read_only_fields = ['offer', 'order_number']


class OfferAcceptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['orderer_acception']
        

class ViewDriversInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['drivers_info']
        depth = 1


class UploadInventoryBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['receipt_id', 'receipt_status', 'bill_rejection_reasons']


class ViewDemurrageBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['demurrage']
        depth = 1


class UploadPaymentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['bill_id', 'bill_status', 'bill_rejection_reasons']


class ConfirmPrepaymentRecieptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['bill_id', 'price', 'payment_date']



class ConfirmPrepaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_id', 'bill_id', 'bill_status', 'receipt_rejection_reasons']
        read_only_fields = ['receipt_id', 'bill_id']


class UploadLoadInfoBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        exclude = ['status','rejection_reasons']


class UploadInvoicePackingBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        exclude = ['status','rejection_reasons']


class ConfirmLadingBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['status','rejection_reasons']
        read_only_fields = ['bill_id']


class ConfirmInventoryReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_status', 'receipt_rejection_reasons', 'receipt_id']
        read_only_fields = ['receipt_id']


class UploadDemurrageReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_id']
        read_only_fields = ['bill_id']


class UploadBijakBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_id']


class DefineSecondDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['second_destination']



class ConfirmSecondDestinationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_status','bill_rejection_reasons','bill_id']
        read_only_fields = ['bill_id']


class OrderCompletionAprroveserializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderer_completion_date']



class UploadDriversInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_id']


class UploadDemurrageBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_id', 'price']


class ConfirmInventoryBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_id', 'bill_status','bill_rejection_reasons']
        read_only_fields = ['bill_id']


class ConfirmDemurrageBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_id', 'bill_status','bill_rejection_reasons']
        read_only_fields = ['bill_id']


class ConfrimPrepaymentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_status','bill_rejection_reasons', 'bill_id']
        read_only_fields = ['bill_id']


class ViewLoadInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['load_info']
        depth = 1


class UploadLadingBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_id']


class UploadInventoryReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_id', 'bill_id']
        read_only_fields = ['bill_id']


class ConfirmDemurrageReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_status', 'receipt_rejection_reasons']
        read_only_fields = ['bill_id']


class ConfirmBijakBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['status', 'rejection_reasons']
        read_only_fields = ['bill_id']


class UploadSecondDestinationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_id']


class ConfirmFinalPaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_status', 'receipt_rejection_reasons']
        read_only_fields = ['bill_id']


class OfferSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['orderer_acception']


class UploadPrepaymentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_id']


class UploadPrepaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receipt_id']


class ViewDealDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperWork
        fields = ['bill_id']


class UploadFinalPaymentReceipt(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['bill_id', 'receipt_id']
        read_only_fields = ['bill_id']


class UploadOrderNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['order_number']


class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['price']
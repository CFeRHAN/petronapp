from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from trader.models import Trader
from freight.models import Freight
from producer.models import Producer
from users.models import User


class Payment(models.Model):
    """model for covering all payment methods"""
    
    bill_file = models.CharField(max_length=35, blank=True, null=True)
    receipt_file = models.CharField(max_length=35, blank=True, null=True)
    price = models.FloatField(blank=False)
    payment_date = models.DateField(null=False, blank=False)
    bill_status = models.BooleanField(default=False)
    bill_rejection_reasons = models.TextField(blank=True)
    receipt_status = models.BooleanField(default=False)
    receipt_rejection_reasons = models.TextField(blank=True)

    def __str__(self):
        return str(self.bill_file)


class PaperWork(models.Model):
    """model for covering all paper works"""
    
    bill_file = models.CharField(max_length=35)
    upload_date = models.DateField(null=False, blank=False)
    status = models.BooleanField(default=False)
    rejection_reasons = models.TextField(blank=True)

    def __str__(self):
        return str(self.bill_file)


class Order(models.Model):
    """Model for the Order submitted by Trader or Petro in which we name it orderer."""

    TYPE_CHOICES = [
        ('0', 'FCA'),
        ('1', 'CPT'),
    ]

    orderer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orderer")
    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="petro_seller_co")        # Producer !!!
    contract_type = models.CharField(max_length=1, choices=TYPE_CHOICES, blank=False, null=False)
    ordering_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    order_number = models.CharField(max_length=35, blank=True, null=True)
    order_number_file = models.CharField(max_length=35, blank=True, null=True)
    product = models.CharField(max_length=200, blank=False, null=False)
    weight = models.FloatField(blank=False, null=False)
    vehicle_type = models.CharField(max_length=200, blank=False, null=False)
    loading_location = models.CharField(max_length=200, blank=False, null=False)
    destination = models.CharField(max_length=200, blank=False, null=False)
    second_destination = models.CharField(max_length=200, blank=True, null=True)
    loading_date = models.DateTimeField(auto_now_add=False, blank=False, null=False)
    border_passage = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    proforma_file = models.CharField(max_length=35)
    orderer_completion_date = models.DateTimeField(null=True, blank=True)  # change this to datetime field
    freight_completion_date = models.DateTimeField(null=True, blank=True)  # change this to datetime field

    class Meta:
        ordering = ['loading_date']

    def __str__(self):
        return f'{self.orderer} - {self.product}'
    
    def current_order(self):
        return Order.objects.filter(order=self, channel=self)


class Offer(models.Model):
    """Model for offers that are made by the Freight company"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    freight = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField(blank=False, null=False)
    orderer_acception = models.BooleanField(default=False, blank=False, null=False)
    freight_acception = models.BooleanField(default=False, blank=False, null=False)
    prepayment_percentage = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(100), MinValueValidator(0)])
    
    # PAYMENT
    # we use revert usecase for bill and reciept in prepayment just not to make another field for confirm prepayment
    prepayment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='prepayment_receipt', null=True, blank=True) 
    demurrage = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='demurrage_price', null=True, blank=True)
    inventory = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='inventory_price', null=True, blank=True)
    second_destination_cost = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='second_destination_cost', null=True, blank=True)
    final_payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='final_payment', null=True, blank=True)

    # BILL
    lading_bill = models.ForeignKey(PaperWork, on_delete=models.DO_NOTHING, related_name='lading_bill', null=True, blank=True)
    drivers_info = models.ForeignKey(PaperWork, on_delete=models.DO_NOTHING, related_name='drivers_info', null=True, blank=True)
    bijak = models.ForeignKey(PaperWork, on_delete=models.DO_NOTHING, related_name='bijak', null=True, blank=True)
    invoice_packing = models.ForeignKey(PaperWork, on_delete=models.DO_NOTHING, related_name='invoice_packing', null=True, blank=True)
    order_number = models.CharField(max_length=35, null=True, blank=True)
    order_number_file = models.CharField(max_length=35, null=True, blank=True)
    order_number_seen_status = models.BooleanField(default=False, null=True, blank=True)
    
    deal_draft = models.ForeignKey(PaperWork, on_delete=models.DO_NOTHING, related_name='prescript', null=False, blank=False)
    load_info = models.ForeignKey(PaperWork, on_delete=models.DO_NOTHING, related_name='load_info', null=True, blank=True)
    seen = models.BooleanField(default=False, null=True, blank=True)


    def get_percentage(self):
        try:
            return self.prepayment_percentage / 100
        except TypeError:
            return 0
    
    def get_prepayment_amount(self):
        try:
            return self.price * self.get_percentage()
        except AttributeError:
            return 0

    def get_remained_amount(self):
        return self.price - self.get_prepayment_amount()
    
    def get_order(self):
        return self.order

    def __str__(self):
        return f'{self.order.orderer} - {self.freight}'
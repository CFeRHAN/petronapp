from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, Offer


@api_view(['GET'])
def flow_manager_api(request, offer_pk):
    user = request.user
    try:
        offer = Offer.objects.get(pk=offer_pk)
    except Offer.DoesNotExist:
        return Response({'message': f'offer {offer_pk} not found'})

    return Response(flow_manager(offer_pk, offer, user))


def flow_manager(offer_pk, offer, user):
    # {'code': 'FMF01', 'text': 'مشاهده شماره سفارش', 'description': 'send order number to frieght'}
        
    if offer.order.contract_type == '1':
        if user.role == '1':
            return _trader_(offer, user)

        if user.role == '2':
            return _freight_(offer, user)
        
        if user.role == '3':
            return _producer_(offer_pk, user)

        else:
            return {'message':'user permission denied'}
    
    return {'message':'Contract Type is not supported'}


def _trader_(offer, user):
    if not offer.order_number_file:
        return {'code': 'FMT01', 'text': 'ارسال شماره سفارش', 'description': 'send order number to frieght'}
    
    if offer.prepayment:
        if not offer.prepayment.bill_file:
            return {'code': 'FMT02', 'text': 'بارگذاری رسید پیش پرداخت', 'description': 'upload prepayment bill'}
        
        if offer.prepayment.receipt_status:
            return {'code': 'FMT03', 'text': 'تایید رسید پیش‌ پرداخت', 'description': 'confirm prepayment receipt'}

    if offer.lading_bill.status == 'False':
        return {'code': 'FMT04', 'text': 'تایید بارنامه', 'description': 'confirm lading bill'}

    if offer.order.freight_completion_date:
        return {'code': 'FMT05', 'text': 'اعلام پایان سفارش', 'description': 'orderer done approval'}

    if offer.order.freight_completion_date and offer.order.orderer_completion_date:
        return {'code': 'FMT06', 'text': 'تایید قبض انبارداری', 'description': 'confirm inventory bill'}
    
    """here should be the second destination trigger"""

    if offer.inventory.bill_status and offer.inventory.bill_file== 'False':
        return {'code': 'FMT07', 'text': 'تایید قبض انبارداری', 'description': 'confirm inventory bill'}

    if offer.inventory.bill_status == 'True' and not offer.inventory.receipt_file:
        return {'code': 'FMT08', 'text': 'بارگذاری رسید انبارداری', 'description': 'upload inventory receipt'}

    if offer.demurrage.bill_file and offer.demurrage.bill_status == 'False':
        return {'code': 'FMT09', 'text': 'تایید قبض دموراژ', 'description': 'confirm demurrage bill'}
    
    if offer.demurrage.bill_status == 'True' and not offer.demurrage.receipt_file:
        return {'code': 'FMT10', 'text': 'بارگذاری رسید دموراژ', 'description': 'upload demurrage receipt'}
    
    if offer.final_payment.bill_file and offer.final_payment.bill_status == 'False':
        return {'code': 'FMT11', 'text': 'تایید قبض پرداخت نهایی', 'description': 'confirm final payment bill'}
    
    if offer.final_payment.bill_status == 'True' and not offer.final_payment.receipt_file:
        return {'code': 'FMT12', 'text': 'بارگذاری رسید پرداخت نهایی', 'description': 'upload final payment receipt'}


def _freight_(offer, user):
    if offer.order_number_file and not offer.order_number_seen_status:
        return {'code': 'FMF01', 'text': 'مشاهده شماره سفارش', 'description': 'view order number'}
    
    if offer.order_number_seen_status and not offer.drivers_info.bill_file:
        return {'code': 'FMF02', 'text': 'بارگذاری فایل معرفی رانندگان', 'description': 'upload drivers info'}
    
    if offer.drivers_info.status and not offer.inventory.bill_file:
        return {'code': 'FMF03', 'text': 'بارگذاری فبض انبارداری', 'description': 'upload inventory bill'}
    
    if offer.inventory.bill_status and not offer.demurrage.bill_status:
        return {'code': 'FMF04', 'text': 'تایید قبض دموراژ', 'description': 'confirm demurrage bill'}
    
    if offer.demurrage.bill_status and not offer.prepayment_percentage:
        return {'code': 'FMF05', 'text': 'مشاهده مشخصات بار', 'description': 'view load info'}
    
    if offer.demurrage.bill_status and offer.prepayment_percentage:
        return {'code': 'FMF06', 'text': 'تایید قبض پیش پرداخت', 'description': 'confirm prepayment bill'}
    
    if offer.prepayment_percentage and not offer.prepayment.bill_status:
        return {'code': 'FMF07', 'text': 'بارگذاری رسید پیش پرداخت', 'description': 'upload prepayment receipt'}
    
    if offer.prepayment.receipt_file and offer.load_info.status == 'False':
        return {'code': 'FMF08', 'text': 'مشاهده مشخصات بار', 'description': 'view load info'}

    if offer.load_info.status and not offer.lading_bill.bill_file:
        return {'code': 'FMF09', 'text': 'بارکذاری فایل بارنامه', 'description': 'upload lading bill'}
    
    if offer.order.border_passage and not offer.bijak.status:
        return {'code': 'FMF10', 'text': 'تایید بیجک', 'description': 'confirm bijak'}
    
    if not offer.order.border_passage and not offer.order.freight_completion_date:
        return {'code': 'FMF11', 'text': 'اعلام رسیدن به مقصد', 'description': 'freight done approval'}
    
    if offer.bijak.status and not offer.order.freight_completion_date:
        return {'code': 'FMF12', 'text': 'اعلام رسیدن به مقصد', 'description': 'freight done approval'}
    
    if offer.order.second_destination and not offer.second_destination_cost.bill_file:
        return {'code': 'FMF13', 'text': 'بارگذاری قبض هزینه‌های حمل به مقصد دوم', 'description':'upload second destination cost bill'}
    
    if offer.second_destination_cost and not offer.inventory.receipt_file:
        return {'code': 'FMF14', 'text': 'بارگذاری رسید پرداخت هزینه‌های انبارداری', 'description': 'upload inventory receipt'}

    if not offer.order.second_destination and offer.order.freight_completion_date:
        return {'code': 'FMF15', 'text': 'بارگذاری رسید پرداخت هزینه‌های انبارداری', 'description': 'upload inventory receipt'}
    
    if offer.inventory.receipt_status:
        return {'description': 'you are done.'}


def _producer_(offer_pk, user):
    offer = Offer.objects.get(id=offer_pk, producer=user)

    if offer.freight_acception == 'True' and not offer.order.order_number:
        return {'code': 'FMP01', 'text': 'بارگذاری فایل شماره سفارش', 'description': 'upload order number'}
    
    if offer.drivers_info.status == 'False':
        return {'code': 'FMP02', 'text': 'مشاهده اطلاعات رانندگان', 'description': 'view drivers info'}
    
    if offer.drivers_info.status == 'True' and not offer.inventory.bill_file:
        return {'code': 'FMP03', 'text': 'بارگذاری قبض هزینه‌های انبارداری', 'description': 'upload inventory bill'}

    if offer.inventory.bill_file and offer.demurrage.bill_status == 'False':
        return {'code': 'FMP04', 'text': 'تایید قبض هزینه‌های دموراژ', 'description': 'confirm demurrage bill'}
    
    if offer.demurrage.bill_status == 'True' and not offer.load_info.bill_file:
        return {'code': 'FMP05', 'text': 'بارگذاری فایل مشخصات بار', 'description': 'upload load info'}

    if offer.load_info.bill_file and offer.order.border_passage:
        return {'code': 'FMP06', 'text': 'بارگذاری فاکتور بسته‌بندی ', 'description': 'upload invoice packing'}
    
    if offer.invoice_packing.bill_file and offer.lading_bill.status == 'False':
        return {'code': 'FMP07', 'text': 'مشاهده فایل بارنامه', 'description': 'view lading bill'}
    
    if offer.lading_bill.status == 'True' and not offer.bijak.bill_file:
        return {'code': 'FMP08', 'text': 'بارگذاری بیجک', 'description': 'upload bijak'}
    
    if (not offer.order.border_passage and offer.load_info.bill_file) or offer.bijak.status:
        return {'code': 'FMP09', 'text': 'تایید قبض هزینه‌های انبارداری', 'description': 'confirm inventory bill'}
    
    if offer.bijak.status == True and offer.inventory.receipt_status == 'False':
        return {'code': 'FMP10', 'text': 'تایید رسید پرداخت هزینه‌های انبارداری', 'description': 'confirm inventory receipt'}
    
    if offer.inventory.receipt_status == 'True' and not offer.demurrage.receipt_file:
        return {'code': 'FMP11', 'text': 'بارگذاری زسید پرداخت هزینه‌های دموراژ', 'description': 'upload demurrage receipt'}

    if offer.demurrage.receipt_status == 'True':
        return {'code': 'FMP12', 'description': 'you are done.'}
    elif offer.demurrage.receipt_status == 'False':
        return {'code': 'FMP13', 'description':'there is an issue with demurrage/inventory file please try uploading it again.'}

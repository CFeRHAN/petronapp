from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, Offer


@api_view(['GET'])
def flow_manager(request, offer_pk):

    user = request.user

    try:
        offer = Offer.objects.get(pk=offer_pk)
    except Offer.DoesNotExist:
        return Response({'message': f'offer {offer_pk} not found'})


    def _trader_():

        if not offer.order_number_file:
            return Response({'next_step': 'send order number to frieght'})
        
        if offer.prepayment:
            if not offer.prepayment.bill_file:
                return Response({'next_step': 'upload prepayment bill'})
            
            if offer.prepayment.receipt_status:
                return Response({'next_step': 'confirm prepayment receipt'})

        if offer.lading_bill.status == 'False':
            return Response({'next_step': 'confirm lading bill'})

        if offer.order.freight_completion_date:
            return Response({'next_step': 'orderer done approval'})

        if offer.order.freight_completion_date and offer.order.orderer_completion_date:
            return Response({'next_step': 'confirm inventory bill'})
        
        """here should be the second destination trigger"""

        if offer.inventory.bill_status and offer.inventory.bill_file== 'False':
            return Response({'next_step': 'confirm inventory bill'})

        if offer.inventory.bill_status == 'True' and not offer.inventory.receipt_file:
            return Response({'next_step': 'upload inventory receipt'})

        if offer.demurrage.bill_file and offer.demurrage.bill_status == 'False':
            return Response({'next_step': 'confirm demurrage bill'})
        
        if offer.demurrage.bill_status == 'True' and not offer.demurrage.receipt_file:
            return Response({'nex_step': 'upload demurrage receipt'})
        
        if offer.final_payment.bill_file and offer.final_payment.bill_status == 'False':
            return Response({'next_step': 'confirm final payment bill'})
        
        if offer.final_payment.bill_status == 'True' and not offer.final_payment.receipt_file:
            return Response({'next_step': 'upload final payment receipt'})


    def _freight_():
        
        if offer.order_number_file and not offer.order_number_seen_status:
            return Response({'next_step': 'view order number'})
        
        if offer.order_number_seen_status and not offer.drivers_info.bill_file:
            return Response({'next_step': 'upload drivers info'})
        
        if offer.drivers_info.status and not offer.inventory.bill_file:
            return Response({'next_step': 'upload inventory bill'})
        
        if offer.inventory.bill_status and not offer.demurrage.bill_status:
            return Response({'next_step': 'confirm demurrage bill'})
        
        if offer.demurrage.bill_status and not offer.prepayment_percentage:
            return Response({'next_step': 'view load info'})
        
        if offer.demurrage.bill_status and offer.prepayment_percentage:
            return Response({'next_step': 'confirm prepayment bill'})
        
        if offer.prepayment_percentage and not offer.prepayment.bill_status:
            return Response({'next_step': 'upload prepayment receipt'})
        
        if offer.prepayment.receipt_file and offer.load_info.status == 'False':
            return Response({'next_step': 'view load info'})
        
        if offer.load_info.status and not offer.lading_bill.bill_file:
            return Response({'next_step': 'upload lading bill'})
        
        if offer.order.border_passage and not offer.bijak.status:
            return Response({'next_step': 'confirm bijak'})
        
        if not offer.order.border_passage and not offer.order.freight_completion_date:
            return Response({'next_step': 'freight done approval'})
        
        if offer.bijak.status and not offer.order.freight_completion_date:
            return Response({'next_step': 'freight done approval'})
        
        if offer.order.second_destination and not offer.second_destination_cost.bill_file:
            return Response({'next_step':'upload second destination bill'})
        
        if offer.second_destination_cost and not offer.inventory.receipt_file:
            return Response({'next_step': 'upload inventory receipt'})
        
        if not offer.order.second_destination and offer.order.freight_completion_date:
            return Response({'next_step': 'upload inventory receipt'})
        
        if offer.inventory.receipt_status:
            return Response({'you are done.'})


    def _producer_():
        
        offer = Offer.objects.get(id=offer_pk, producer=user)

        if offer.freight_acception == 'True' and not offer.order.order_number:
            return Response({'next_step': 'upload order number'})
        
        if offer.drivers_info.status == 'False':
            return Response({'next_step': 'view_drivers info'})
        
        if offer.drivers_info.status == 'True' and not offer.inventory.bill_file:
            return Response({'next_step': 'upload inventory bill'})

        if offer.inventory.bill_file and offer.demurrage.bill_status == 'False':
            return Response({'next_step': 'confirm demurrage bill'})
        
        if offer.demurrage.bill_status == 'True' and not offer.load_info.bill_file:
            return Response({'next_step': 'upload load info'})

        if offer.load_info.bill_file and offer.order.border_passage:
            return Response({'next_step': 'upload invoice packing'})
        
        if offer.invoice_packing.bill_file and offer.lading_bill.status == 'False':
            return Response({'next_step': 'view lading bill'})
        
        if offer.lading_bill.status == 'True' and not offer.bijak.bill_file:
            return Response({'next_step': 'upload bijak'})
        
        if (not offer.order.border_passage and offer.load_info.bill_file) or offer.bijak.status:
            return Response({'next_step': 'confirm inventory bill'})
        
        if offer.bijak.status == True and offer.inventory.receipt_status == 'False':
            return Response({'next_step': 'confirm inventory receipt'})
        
        if offer.inventory.receipt_status == 'True' and not offer.demurrage.receipt_file:
            return Response({'next_step': 'upload demurrage receipt'})

        if offer.demurrage.receipt_status == 'True':
            return Response({'next_step': 'you are done.'})
        elif offer.demurrage.receipt_status == 'False':
            return Response({'next_step':'there is an issue with demurrage/inventory file please try uploading it again.'})

        
    if offer.order.contract_type == '1':

        if user.role == '1':
            return _trader_()

        if user.role == '2':
            return _freight_()
        
        if user.role == '3':
            return _producer_()

        else:
            return Response({'message':'user permission denied'})
    
    return Response({'message':'Contract Type is not supported'})
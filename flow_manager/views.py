from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, Offer


# @api_view(['GET'])
# def flow_manager(request, order_pk, offer_pk, format=None):
#     user = request.user

#     try:
#         order = Order.objects.get(pk=order_pk)
#     except Order.DoesNotExist:
#         return Response({'next_step': 'Go create an order'}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         offer = Offer.objects.get(pk=offer_pk, order=order_pk)
#     except Offer.DoesNotExist:
#         return Response({'next_step': 'Wait for an offer'}, status=status.HTTP_404_NOT_FOUND)


#     try:
#         if offer.final_payment.receipt_status != None and offer.final_payment.receipt_status == True:
#             return Response({'next_step': 'you are done!'}, status=status.HTTP_200_OK)
#     except AttributeError:
#         return Response({'message': 'there is no final payment'}, status=status.HTTP_404_NOT_FOUND)
    
#     if offer.final_payment.receipt_file != None:
#         return Response({'next_step': 'final_payment_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif offer.inventory.receipt_status == True:
#         return Response({'next_step':'upload_final_payment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)
    
#     elif offer.inventory.receipt_file != None:
#         return Response({'next_step': 'inventory_receipt_confirmation', 'user_role':'3'}, status=status.HTTP_200_OK)
    
#     elif offer.demurrage.receipt_status == True:
#         return Response({'next_step':'final_payment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)

#     elif offer.demurrage.receipt_file != None:
#         return Response({'next_step': 'inventory_receipt_confirmation', 'user_role':'3'}, status=status.HTTP_200_OK)

#     elif order.orderer_completion_date != None:
#         return Response({'next_step': 'upload_demurrage/inventory_receipt', 'user_role':'2'}, status=status.HTTP_200_OK)

#     elif order.second_destination != None:
#         return Response({'next_step': 'orderer_completion_approval', 'user_role':'1'}, status=status.HTTP_200_OK)

#     elif order.freight_completion_date !=None:
#         return Response({'next_step': 'orderer_completion_approval or second_destination', 'user_role':'1'})
    
#     elif offer.bijak.status == True:
#         return Response({'next_step':'freight_completion_approval', 'user_role':'2'}, status=status.HTTP_200_OK)

#     elif offer.bijak.bill_file != None:
#         return Response ({'next_step':'bijak_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif offer.lading_bill.status == True:
#         return Response({'next_step': 'upload_bijak bill', 'user_role':'3'}, status=status.HTTP_200_OK)
    
#     elif offer.lading_bill.bill_file != None:
#         return Response({'next_step': 'lading_bill_confirmation', 'user_role':'1'}, status=status.HTTP_200_OK)

#     elif offer.invoice_packing.status == True:
#         return Response({'next_step': 'upload_lading_bill', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif offer.invoice_packing.bill_file != None:
#         return Response({'next_step': 'invocie_packing_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif offer.load_info.bill_file != None:
#         return Response({'next_step': 'upload_invoice_packing', 'user_role':'3'}, status=status.HTTP_200_OK)

#     elif offer.prepayment.bill_status == True:
#         return Response({'next_step': 'upload_load_info bill', 'user_role':'3'}, status=status.HTTP_200_OK)
    
#     elif offer.prepayment.receipt_file != None:
#         return Response({'next_step': 'prepayment_reciept_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif offer.demurrage.bill_status == True:
#         return Response({'next_step':'upload_prepayment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)

#     elif offer.demurrage.receipt_file != None:
#         return Response({'next_step': 'inventory_receipt_confirmation', 'user_role':'3'}, status=status.HTTP_200_OK)
        
#     elif offer.inventory.bill_status == True:
#         return Response({'next_step':'upload_prepayment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)

#     elif offer.inventory.bill_file != None:
#         return Response({'next_step': 'inventory_bill_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)

#     elif offer.drivers_info != None:
#         return Response({'next_step': 'the_inventory_bill', 'user_role':'3'}, status=status.HTTP_200_OK)
    
#     elif offer.order_number != None:
#         return Response({'next_step': 'drivers_info', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif order.order_number != None:
#         if order.contract_type == "FCA":
#             return Response({'next_step': 'send_order_number', 'user_role':'1'}, status=status.HTTP_200_OK)
#         elif order.contract_type == "CPT":
#             return Response({'next_step': 'upload_drivers_info', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     elif offer.orderer_acception == True:
#         return Response({'next_step': 'upload_order_number', 'user_role':'2'}, status=status.HTTP_200_OK)
    
#     else:
#         return Response({'failed': 'cant recognize the flow'}, status=status.HTTP_400_BAD_REQUEST)


    

@api_view(['GET'])
def flow(offer_pk, request):
    user = request.user

    if user.role == '1':
        _trader_(offer_pk)
    
    if user.role == '2':
        _freight_(offer_pk)
    
    if user.role == '3':
        _producer_(offer_pk)


    def _trader_(offer_pk):
        offer = Offer.objects.get(pk=offer_pk, freight_acception=True)

        order = offer.order.id
        order = Order.objects.get(pk=order)

        if not offer.order_number:
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

    def _freight_(offer_pk):
        
        offer = Offer.objects.get(pk=offer_pk)

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

        pass

    def _producer_(offer_pk):
        
        offer = Offer.objects.get(id=offer_pk, producer=user)
        order = Order.objects.get(id=offer.order.id)

        if offer.freight_acception == 'True' and not order.order_number:
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

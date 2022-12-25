from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, Offer


@api_view(['GET'])
def flow_manager(request, order_pk, offer_pk, format=None):
    user = request.user

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response({'next_step': 'Go create an order'}, status=status.HTTP_404_NOT_FOUND)

    try:
        offer = Offer.objects.get(pk=offer_pk, order=order_pk)
    except Offer.DoesNotExist:
        return Response({'next_step': 'Wait for an offer'}, status=status.HTTP_404_NOT_FOUND)


    if offer.final_payment.status == True:
        return Response({'next_step': 'you are done!'}, status=status.HTTP_200_OK)
    
    elif offer.final_payment.receipt_file != None:
        return Response({'next_step': 'final_payment_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif offer.inventory.receipt_status == True:
        return Response({'next_step':'upload_final_payment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)
    
    elif offer.inventory.receipt_file != None:
        return Response({'next_step': 'inventory_receipt_confirmation', 'user_role':'3'}, status=status.HTTP_200_OK)
    
    elif offer.demurrage.receipt_status == True:
        return Response({'next_step':'final_payment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)

    elif offer.demurrage.receipt_file != None:
        return Response({'next_step': 'inventory_receipt_confirmation', 'user_role':'3'}, status=status.HTTP_200_OK)

    elif order.orderer_completion_date != None:
        return Response({'next_step': 'upload_demurrage/inventory_receipt', 'user_role':'2'}, status=status.HTTP_200_OK)

    elif order.second_destination != None:
        return Response({'next_step': 'orderer_completion_approval', 'user_role':'1'}, status=status.HTTP_200_OK)

    elif order.freight_completion_date !=None:
        return Response({'next_step': 'orderer_completion_approval or second_destination', 'user_role':'1'})
    
    elif offer.bijak.status == True:
        return Response({'next_step':'freight_completion_approval', 'user_role':'2'}, status=status.HTTP_200_OK)

    elif offer.bijak.bill_file != None:
        return Response ({'next_step':'bijak_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif offer.lading_bill.status == True:
        return Response({'next_step': 'upload_bijak bill', 'user_role':'3'}, status=status.HTTP_200_OK)
    
    elif offer.lading_bill.bill_file != None:
        return Response({'next_step': 'lading_bill_confirmation', 'user_role':'1'}, status=status.HTTP_200_OK)

    elif offer.invoice_packing.status == True:
        return Response({'next_step': 'upload_lading_bill', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif offer.invoice_packing.bill_file != None:
        return Response({'next_step': 'invocie_packing_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif offer.load_info.bill_file != None:
        return Response({'next_step': 'upload_invoice_packing', 'user_role':'3'}, status=status.HTTP_200_OK)

    elif offer.prepayment.bill_status == True:
        return Response({'next_step': 'upload_load_info bill', 'user_role':'3'}, status=status.HTTP_200_OK)
    
    elif offer.prepayment.receipt_file != None:
        return Response({'next_step': 'prepayment_reciept_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif offer.demurrage.bill_status == True:
        return Response({'next_step':'upload_prepayment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)

    elif offer.demurrage.receipt_file != None:
        return Response({'next_step': 'inventory_receipt_confirmation', 'user_role':'3'}, status=status.HTTP_200_OK)
        
    elif offer.inventory.bill_status == True:
        return Response({'next_step':'upload_prepayment_reciept', 'user_role':'1'}, status=status.HTTP_200_OK)

    elif offer.inventory.bill_file != None:
        return Response({'next_step': 'inventory_bill_confirmation', 'user_role':'2'}, status=status.HTTP_200_OK)

    elif offer.drivers_info != None:
        return Response({'next_step': 'the_inventory_bill', 'user_role':'3'}, status=status.HTTP_200_OK)
    
    elif offer.order_number != None:
        return Response({'next_step': 'drivers_info', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif order.order_number != None:
        if order.contract_type == "FCA":
            return Response({'next_step': 'send_order_number', 'user_role':'1'}, status=status.HTTP_200_OK)
        elif order.contract_type == "CPT":
            return Response({'next_step': 'upload_drivers_info', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    elif offer.orderer_acception == True:
        return Response({'next_step': 'upload_order_number', 'user_role':'2'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'failed': 'cant recognize the flow'}, status=status.HTTP_400_BAD_REQUEST)


    

    
    


    # if offer.lading_bill != None:
    #     return Response({'next_step': 'drivers_info'}, status=status.HTTP_200_OK)
    
    # elif offer.drivers_info != None:
    #     return Response({'next_step': 'bijak'}, status=status.HTTP_200_OK)

    # elif offer.bijak != None:
    #     return Response({'next_step': 'invoice_packing'}, status=status.HTTP_200_OK)
    
    # elif offer.invoice_packing != None:
    #     return Response({'next_step': 'order_number'}, status=status.HTTP_200_OK)
    
    # elif offer.order_number != None:
    #     return Response({'next_step': 'load_info'}, status=status.HTTP_200_OK)
    
    # elif offer.load_info != None:
    #     return Response({'next_step': 'prepayment'}, status=status.HTTP_200_OK)
    
    # elif offer.prepayment != None:
    #     return Response({'next_step': 'demurrage'}, status=status.HTTP_200_OK)
    
    # elif offer.demurrage != None:
    #     return Response({'next_step': 'inventory'}, status=status.HTTP_200_OK)
    
    # elif offer.inventory != None:
    #     return Response({'next_step': 'second_destination_cost'}, status=status.HTTP_200_OK)
    
    # elif offer.final_payment != None:
    #     return Response({'next_step': 'you are done already'}, status=status.HTTP_200_OK)

    
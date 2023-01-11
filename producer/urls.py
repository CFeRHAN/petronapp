from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [

    path('profile/', profile, name='create_profile'),
    
    path('orders/', orders, name='producer_orders'),
    path('recieved_orders/', recieved_orders, name='recieved_orders'),
    path('orders/<int:order_pk>/', order_detail, name='order_detail'),
    path('orders/<int:order_pk>/offers/', offers, name='offers'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/', offer_detail, name='producer_offer_detail'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/offer_acception/', offer_acception, name='offer_acception'),
    path('orders/approved_offers/', approved_offers, name='approved_offers'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/order_number/', upload_order_number, name='upload_order_number'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/drivers_info/', view_drivers_info, name='view_drivers_info'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/invetory_bill/', upload_invetory_bill, name='upload_invetory_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_bill/', view_demurrage_bill, name='view_demurrage_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/prepayment_bill/', upload_prepayment_bill, name='upload_prepayment_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/prepayment_receipt/', confirm_prepayment_receipt, name='confirm_prepayment_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/load_information/', upload_load_information, name='upload_load_information'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/invoice_packing_bill/', upload_invoice_packing_bill, name='upload_invoice_packing_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/lading_bill/', confirm_lading_bill, name='confirm_lading_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_receipt/', upload_demurrage_receipt, name='upload_demurrage_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/bijak/', upload_bijak, name='upload_bijak'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/second_destination/', define_second_destination, name='define_second_destination'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/second_destination_bill/', confirm_second_destination_bill, name='confirm_second_destination_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/completion_approval/', order_completion_approval, name='order_completion_approval'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/final_payment_receipt/', upload_final_payment_receipt, name='upload_final_payment_receipt'),


    path('', view_all_producers, name='get_all_producers'),
]

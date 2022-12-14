from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [

    path('profile/<int:pk>/', create_profile, name='create_profile'),
    
    path('orders/', orders, name='orders'),
    path('orders/<int:order_pk>/', order_detail, name='order_detail'),
    path('orders/<int:order_pk>/offers/', offers, name='offers'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/', offer_detail, name='offer_detail'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/offer_acception/', offer_acception, name='offer_acception'),
    path('orders/approved/', approved_orders, name='approved_orders'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/deal_draft/', view_deal_draft, name='view_deal_draft'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/order_number/', send_order_number, name='send_order_number'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/prepayment_bill/', upload_prepayment_bill, name='upload_prepayment_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/prepayment_receipt/', confirm_prepayment_receipt, name='confirm_prepayment_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/lading_bill/', confirm_lading_bill, name='confirm_lading_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/inventory_bill/', confirm_inventory_bill, name='confirm_inventory_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_bill/', confirm_demurrage_bill, name='confirm_demurrage_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/inventory_receipt/', upload_inventory_receipt, name='upload_inventory_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_receipt/', upload_demurrage_receipt, name='upload_demurrage_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/completion_approval/', order_completion_approval, name='order_completion_approval'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/second_destination/', define_second_destination, name='define_second_destination'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/second_destination_bill/', confirm_second_destination_bill, name='confirm_second_destination_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/final_payment_receipt/', upload_final_payment_receipt, name='upload_final_payment_receipt'),

]

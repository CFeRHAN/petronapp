from django.urls import path

from .views import *


urlpatterns = [
    path('profile/<int:pk>/', profile, name='create_profile'),
    path('orders/', orders, name='freight_orders'),
    path('orders/<int:order_pk>/', order_detail, name='freight_order_detail'),
    path('orders/<int:order_pk>/create_offer/', create_offer, name='freight_create_offer'),
    path('orders/<int:order_pk>/update_offer/', update_offer, name='freight_update_offer'),
    path('orders/<int:order_pk>/offers/', offers, name='freight_offers'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/', offer_detail, name='freight_offer_detail'),
    path('orders/offer_wait_list/', offer_wait_list, name='offer_wait_list'),
    path('orders/accepted_offers/', accepted_offers, name='accepted_offers'),
    path('orders/nonaccepted_offers/', nonaccepted_offers, name='nonaccepted_offers'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/offer_confirmation/', offer_confirmation, name='offer_confirmation'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/order_number/', view_order_number, name='view_order_number'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/drivers_info/', upload_drivers_info, name='upload_drivers_info'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_bill/', upload_demurrage_bill, name='upload_demurrage_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/inventory_bill/', confirm_inventory_bill, name='confirm_inventory_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/prepayment_bill/', confrim_prepayment_bill, name='confrim_prepayment_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/prepayment_receipt/', upload_prepayment_reciept, name='upload_prepayment_reciept'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/load_information/', view_load_information, name='view_load_information'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/lading_bill/', upload_lading_bill, name='upload_lading_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/inventory_receipt/', upload_inventory_receipt, name='upload_inventory_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_receipt/', confirm_demurrage_receipt, name='confirm_demurrage_receipt'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/bijak_bill/', confirm_bijak_bill, name='confirm_bijak_bill'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/completion_approval/', order_completion_approval, name='order_completion_approval'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/second_destination_cost/', upload_second_destination_cost, name='upload_second_destination_cost'),
    path('orders/<int:order_pk>/offers/<int:offer_pk>/final_payment_receipt/', confirm_final_payment_receipt, name='confirm_final_payment_receipt'),

]

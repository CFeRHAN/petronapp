from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    # TRADER ENDPOINTS
    path('trader/orders/', trader_orders, name='trader_orders'),
    # path('trader/orders/<int:order_pk>/', trader_order_detail, name='trader_orders'),
    # path('trader/orders/<int:order_pk>/offers/', trader_offers, name='trader_offers'),
    # path('trader/orders/<int:order_pk>/offers/<int:offer_pk>/', trader_offer_detail, name='trader_offer_detail'),
    # path('trader/orders/approved/', trader_approved_orders, name='trader_approved_orders'),
    # path('trader/orders/<int:order_pk>/approved/', trader_approved_order_detail, name='trader_approved_order_detail'),
    # path('trader/orders/<int:order_pk>/offers/<int:offer_pk>/payment_reciept/', trader_payment_reciept, name='trader_payment_reciept'),
    # path('trader/orders/<int:order_pk>/offers/<int:offer_pk>/lading_bill/', trader_lading_bill, name='trader_lading_bill'),
    # path('trader/orders/<int:order_pk>/offers/<int:offer_pk>/checkout_bill/', trader_checkout_bill, name='trader_checkout_bill'),
    # path('trader/orders/<int:order_pk>/done_approval', trader_approval, name='trader_done_approval'),

    # # ORDERS ENDPOINTS
    # path('orders/<int:order_pk>/offer_counter/', offer_counter, name='offer_counter'),
    # path('orders/<int:order_pk>/approval_check/', approval_check, name='approval_check'),

    # # EXPRESS ENDPOINTS
    # path('express/orders/', express_orders, name='express_orders'),
    # path('express/orders/<int:order_pk>/', express_order_detail, name='express_orders'),
    # path('express/orders/<int:order_pk>/offers/', express_offers, name='express_offers'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/', express_offer_detail, name='express_offer_detail'),

    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/payment_reciept/', express_payment_reciept, name='express_payment_reciept'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/lading_bill/', express_lading_bill, name='express_lading_bill'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/checkout_bill/', express_checkout_bill, name='express_checkout_bill'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/drivers_info/', express_drivers_info, name='express_drivers_info'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_bill/', express_demurrage_bill, name='express_demurrage_bill'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/inventory_bill/', express_inventory_bill, name='express_inventory_bill'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/invoice_bill/', express_invoice_bill, name='express_invoice_bill'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/other_bill/', express_other_bills, name='express_other_bills'),
    # path('express/orders/<int:order_pk>/offers/<int:offer_pk>/checkout_bill/', express_checkout_bill, name='express_checkout_bill'),
    # path('express/orders/<int:order_pk>/done_approval/', express_approval, name='express_done_approval'),

    # # PETRO ENDPOINTS

    # path('petro/orders/expresses/', petro_express, name='petro_express'),
    # path('petro/orders/approved/', petro_approved_orders, name='petro_approved_orders'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/order_number/', petro_order_number, name='petro_order_number'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/drivers_info/', petro_drivers_info, name='petro_drivers_info'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_bill/', petro_demurrage_bill, name='petro_demurrage_bill'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_payment/', petro_demurrage_payment, name='petro_demurrage_payment'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/inventory_bill/', petro_inventory_bill, name='petro_inventory_bill'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/inventory_receipt/', petro_inventory_receipt, name='petro_inventory_receipt'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/packaging_bill/', petro_packaging_bill, name='petro_packaging_bill'),
    # path('petro/orders/<int:order_pk>/offers/<int:offer_pk>/invoice_bill/', petro_invoice_bill, name='petro_invoice_bill'),


]

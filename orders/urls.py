from django.urls import path

from .views import *


urlpatterns = [

    path('orders/', order_dynamic_filter, name='orders'),
    path('orders/<int:offer_pk>/', seen_offer, name='seen_offer'),
    path('<int:order_pk>/offers/<int:offer_pk>/process_checkout/', process_checkout, name='process_checkout'),
    # path('orders/<int:order_pk>/', order_detail, name='order_detail'),
    # path('orders/<int:order_pk>/offers/', offers, name='offers'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/', offer_detail, name='offer_detail'),
    # path('orders/approved/', approved_orders, name='approved_orders'),
    # path('orders/<int:order_pk>/approved/', approved_order_detail, name='approved_order_detail'),
    # path('orders/<int:order_pk>/offer_counter/', offer_counter, name='offer_counter'),

    # path('orders/<int:order_pk>/offers/<int:offer_pk>/payment_reciept/', payment_reciept, name='payment_reciept'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/lading_bill/', lading_bill, name='lading_bill'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/checkout_bill/', checkout_bill, name='checkout_bill'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/drivers_info/', drivers_info, name='drivers_info'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/demurrage_bill/', demurrage_bill, name='demurrage_bill'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/inventory_bill/', inventory_bill, name='inventory_bill'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/invoice_bill/', invoice_bill, name='invoice_bill'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/other_bill/', other_bills, name='other_bills'),
    # path('orders/<int:order_pk>/offers/<int:offer_pk>/checkout_bill/', checkout_bill, name='checkout_bill'),

]
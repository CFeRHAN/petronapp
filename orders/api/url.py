from django.urls import path

from .viewsq import *


urlpatterns = [

    ### Trader ###
    path('trader_order_list/', TraderOrdersListView.as_view(), name='trader_order_list'),
    path('trader_order_detail/<int:pk>/', TraderOrderDetailView.as_view(), name='trader_order_list'),
    path('offer_list/', OfferListView.as_view(), name='offer_list'),
    path('offer_detail/', OfferDetailView.as_view(), name='offer_detail'),
    path('agreed_orders/', AgreedOrdersView.as_view(), name='agreed_orders'),
    path('agreed_order/', AgreedOrdersDetailView.as_view(), name='agreed_order_detail'),
    path('upload_payment_reciept/', UploadPaymentRecieptView.as_view(), name='upload_payment_reciept'),
    path('confirm_ladings/<int:pk>/', ConfirmLadingBillView.as_view(), name='confirm_ladings'),
    path('upload_checkout_bill/<int:pk>/', UploadCheckoutBillView.as_view(), name='upload_checkout_bill'),
    path('offer_count/', OfferCountView.as_view(), name='offer_count'),

    ### Express ###
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('create_offer/', CreateOfferView.as_view(), name='create_offer'),
    path('offer_detail_update/<int:pk>/', OfferDetailUpdate.as_view(), name='offer_detail_update'),
    path('order_number/<int:pk>/', OrderNumberView.as_view(), name='order_number'),
    path('upload_drivers_info/', UploadDriversInformationView.as_view(), name='upload_drivers_info'),
    path('upload_demurrage_bill/', UploadDemurrageBill.as_view(), name='upload_demurrage_bill'),
    path('confirm_inventory/<int:pk>/', ConfirmInventoryBillView.as_view(), name='confirm_inventory'),
    path('packaging_bill/', PackagingBillView.as_view(), name='packaging_bill'),
    path('upload_lading_bill/<int:pk>/', UploadLadingBillView.as_view(), name='upload_lading_bill'),
    path('confirm_invoices/<int:pk>/', ConfirmInvoiceBillView.as_view(), name='confirm_invoices'),
    path('upload_other_bill/<int:pk>/', UploadOtherPricesBillView.as_view(), name='upload_other_bill'),
    path('confirm_checkout_bill/<int:pk>/', ConfirmCheckoutBillView.as_view(), name='confirm_checkout_bill'),

]
from django.urls import path

from .views import *


urlpatterns = [

    path('flow/<int:order_pk>/<int:offer_pk>/', flow, name='flow_manager'),

]
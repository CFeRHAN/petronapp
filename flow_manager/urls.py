from django.urls import path

from .views import *


urlpatterns = [

    path('flow/<int:offer_pk>/', flow, name='flow_manager'),
    path('flow_manage/<int:offer_pk>/', flow_manager, name='flow_managering'),

]
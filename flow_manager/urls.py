from django.urls import path

from .views import *


urlpatterns = [

    path('flow_manage/<int:offer_pk>/', flow_manager_api, name='flow_managering'),

]
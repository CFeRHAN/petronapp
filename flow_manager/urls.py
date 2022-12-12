from django.urls import path

from .views import *


urlpatterns = [

    path('flow/', flow_manager, name='flow_manager'),

]
from django.urls import path

from .views import *

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login, name='login'),
    # path('user/', user_view, name='user_view'),
    # path('logout/', logout, name='logout'),

    path('otp/', OTPView.as_view(),  name='otp_view'),
    path('update_password/', update_password,  name='update_password')

]
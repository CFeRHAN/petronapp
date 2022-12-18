import random
import string
import uuid
from datetime import timedelta
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from utils.senders import send_otp

from file_manager.models import Attachment


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, mobile, role=0, password=None):
        """create a new user profile"""

        if not mobile:
            raise ValueError('User Must Provide Mobile Number')

        user = self.model(mobile=mobile, role=role)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, mobile, password, role="1"):
        """create and save a new superuser with given details"""
        user = self.create_user(mobile=mobile, role="0", password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Default User Model"""

    TYPE_CHOICES = [
    ('0', 'Unknown'),
    ('1', 'Individual Person'),
    ('2', 'Legal Person'),
    ]

    ROLE_CHOICES = [
    ('0', 'Unknows'),
    ('1', 'Trader'),
    ('2', 'Freight'),
    ('3', 'Producer'),
    ]

    NATIONALITY_CHOICES = [
    ('0', 'Iranian'),
    ('1', 'Foreign')
    ]

    username = None
    profile_picture_file = models.CharField(max_length=35)
    mobile = models.CharField(max_length=12, unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, default="0")                                        # حقیقی/ حقوقی
    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default="0")                                        # نقش بازیگر(تریدر- تولیدکننده)
    company_name = models.CharField(max_length=50)                                                                  #نام شرکت
    company_origin = models.CharField(choices=NATIONALITY_CHOICES, max_length=50, default="0")                      #ملیت شرکت
    company_id = models.CharField(max_length=10)                                                                    #شماره ثبت
    company_national_id = models.CharField(max_length=10)                                                           #شناسه ملی
    company_phone = models.CharField(max_length=11, blank=True, null=True)     # DONT need to be unique             #شماره تماس شرکت
    company_fax = models.CharField(max_length=11, blank=True, null=True)                                            #فکس
    url = models.CharField(max_length=255)                                                                          #نشانی اینترنتی
    company_address = models.TextField()                                                                            #آدرس شرکت
    ceo_name = models.CharField(max_length=50)                                                                      #نام مدیر عامل
    agent_name = models.CharField(max_length=50)                                                                    #نام نماینده
    agent_phone = models.CharField(max_length=11, blank=True, null=True)       # DONT need to be unique             #شماره تماس نماینده
    agent_email = models.EmailField()                                                                               # ایمیل نماینده شرکت
    license_file = models.CharField(max_length=35)            #اساسنامه
    company_doc_file = models.CharField(max_length=35)    #فایل ثبت شرکت
    
    about = models.TextField()                                                                                      #درباره شرکت
    email = models.EmailField()                                                                                     #ایمیل شرکت

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(blank=False, null=True, default=False)
    is_superuser = models.BooleanField(blank=False, null=True, default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return self.mobile

class OtpRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=900),

        ).exists()

class OTPManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)


    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp



def _generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return  ''.join(digits)


class OTP(models.Model):
    class OtpChannel(models.TextChoices):
        PHONE = 'Phone'
        EMAIL = 'E-Mail'

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    channel = models.CharField(max_length=10, choices=OtpChannel.choices, default=OtpChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=_generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()
import jwt, datetime
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken 

from django.contrib.auth import get_user_model


from .serializers import *
from users.models import OTP


class OTPView(APIView):
    def get(self, request):
        serializer = RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTP.objects.generate(data)
                return Response(data=RequestOTPResponseSerializer(otp).data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTP.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                return Response(self._handle_login(data))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handle_login(self, otp):
        User = get_user_model()
        query = User.objects.filter(mobile=otp['receiver'])
        if query.exists():
            created = False
            user = query.first()
        else:
            user = User.objects.create(mobile=otp['receiver'])
            created = True

        refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'created':created,
            'user_role': user.role
        }).data


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        mobile = request.data['mobile']
        password = request.data['password']

        user = User.objects.get(mobile=mobile)
        if user is None:
            raise AuthenticationFailed('user not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='H256').decode('utf-8')

        return Response({'jwt': 'token'})


@api_view(['POST'])
def update_password(request, password, new_password):
    user = request.user

    a = user.set_password(password)

    if user.password == a:
        user.set_password(new_password)
        

    return Response({'success':'now you can login with your new password'}, status=status.HTTP_200_OK)



# @api_view(['POST'])
# def register(request):
#     serializer = UserSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view(['POST'])
# def login(request):
#     mobile = request.data['mobile']
#     password = request.data['password']

#     user = User.objects.filter(mobile=mobile).first()

#     if user is None:
#         raise AuthenticationFailed('User not found!')

#     if not user.check_password(password):
#         raise AuthenticationFailed('Incorrect password!')

#     payload = {
#         'id': user.id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#         'iat': datetime.datetime.utcnow()
#     }

#     token = jwt.encode(payload, 'secret', algorithm='HS256')

#     response = Response()

#     response.set_cookie(key='jwt', value=token, httponly=True)
#     response.data = {
#         'jwt': token
#     }
#     return response
    

# @api_view(['GET'])
# def user_view(request):
#     token = request.COOKIES.get('jwt')

#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')

#     try:
#         payload = jwt.decode(token, 'secret', algorithm=['HS256'])
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('Unauthenticated!')

#     user = User.objects.filter(id=payload['id']).first()
#     serializer = UserSerializer(user)
#     return Response(serializer.data)


# @api_view(['POST'])
# def logout(request):
#     response = Response()
#     response.delete_cookie('jwt')
#     response.data = {
#         'message': 'success'
#     }
#     return response

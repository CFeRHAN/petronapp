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
from utils.validator import mobile_validator



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
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


    @swagger_auto_schema(request_body=VerifyOtpRequestSerializer)
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
            'user_role': user.role,
            'user_id': user.id,
            'company_name': user.company_name,
            'profile_picture_file': user.profile_picture_file,

        }).data


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):

        if '@' in request.data['username']:
            profile = User.objects.filter(email=request.data['username'])
            if profile.count() > 1:
                Response({'message':'لطفا با موبایل وارد شوید'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            mobile = mobile_validator(request.data['username'])

        password = request.data['password']
        user = User.objects.get(mobile=mobile)
        if user is None:
            return Response({'message':'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({'message':'incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow()
        }
        
        refresh = RefreshToken.for_user(user)

        return Response(ObtainTokenSerializer({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'created': False,
            'user_role': user.role,
            'user_id': user.id,
            'company_name': user.company_name,
            'profile_picture_file': user.profile_picture_file,

        }).data, status=status.HTTP_200_OK)



@swagger_auto_schema(methods=['POST'], request_body=UpdatePasswordSerializer)
@api_view(['POST'])
def update_password(request):
    user = request.user
    if user.role != '0':
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(serializer.validated_data['password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'password does not match'})
    else:
        return Response({'message':'user has no role'}, status=status.HTTP_401_UNAUTHORIZED)
        





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

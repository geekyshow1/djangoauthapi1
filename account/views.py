from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import PhoneNumberCheckerSerializer,SendPasswordResetEmailSerializer,UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return refresh

class PhoneNumberCheckerView(APIView):
    serializer_class = PhoneNumberCheckerSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception= True):
            return Response({'message': 'Phone number unregisterd.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    print(user)
    token = get_tokens_for_user(user)
    acess_token =str(token.access_token)
    response = Response()
    response.set_cookie(key='refresh_token', value= token, httponly=True)
    response.data = {
      'acess_token': str(acess_token),
      'msg':'Registration Successful'
      }
    return response
  
  
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.data.get('phone_number')
    password = serializer.data.get('password')
    user = authenticate(phone_number=phone_number, password=password)
    if user is None:
      return Response({'errors':{'non_field_errors':['phone_number or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    token = get_tokens_for_user(user)
    acess_token =str(token.access_token)
    response = Response()
    response.set_cookie(key='refresh_token', value= token, httponly=True)
    response.data = {
      'acess_token': str(acess_token),
      'msg':'loged in Successfully'
      }
    return response
class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        response = Response()
        response.delete_cookie('refresh_token')
        response.data = {
            'msg': 'Logout Successful'
        }
        return response

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserModel
from .serializers import UserSerializer
from Card.serializers import CardSerializer
from Address.serializers import AddressSerializer
from Address.models import AddressModel
from Card.models import CardModel

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

class TokenValidateView(APIView):
    def post(self, request):
        print('validate request: ', request)
        token = request.headers.get('Authorization', '').split(' ')[1]
        try:
            UntypedToken(token)  
            return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
        except TokenError as e:
            print('Erro:', e)
            return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

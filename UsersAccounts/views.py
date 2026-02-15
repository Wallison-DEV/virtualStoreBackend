from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.permissions import AllowAny

from .serializers import CustomTokenObtainPairSerializer
from .models import UserModel
from .serializers import UserSerializer
from Companies.models import CompanyModel


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

class TokenValidateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header:
            return Response({'error': 'No token provided'}, status=400)
            
        token = auth_header.split(' ')[1]

        try:
            decoded_token = UntypedToken(token)
            user_id = decoded_token.payload.get('user_id')
            is_company = decoded_token.payload.get('is_company', False)

            if is_company:
                account = CompanyModel.objects.filter(id=user_id).first()
                from Companies.serializers import CompanySerializer
                serializer = CompanySerializer(account)
            else:
                account = UserModel.objects.filter(id=user_id).first()
                from .serializers import UserSerializer
                serializer = UserSerializer(account)

            if not account:
                return Response({'error': 'Account not found'}, status=404)

            return Response(serializer.data, status=200)

        except TokenError:
            return Response({'error': 'Invalid or expired token'}, status=401)

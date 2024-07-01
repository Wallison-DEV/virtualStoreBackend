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
from Companies.models import CompanyModel
from Companies.serializers import CompanySerializer

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer

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
        token = request.headers.get('Authorization', '').split(' ')[1]

        try:
            untyped_token = UntypedToken(token)

            if 'user_id' in untyped_token.payload:
                user_id = untyped_token.payload['user_id']
                try:
                    user = UserModel.objects.get(id=user_id)
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except UserModel.DoesNotExist:
                    return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            elif 'company_id' in untyped_token.payload:
                company_id = untyped_token.payload['company_id']
                try:
                    company = CompanyModel.objects.get(id=company_id)
                    serializer = CompanySerializer(company)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except CompanyModel.DoesNotExist:
                    return Response({'error': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

        except TokenError as e:
            return Response({'error': 'Token inválido', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

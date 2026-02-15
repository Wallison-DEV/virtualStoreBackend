from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models # Import necessário para o Q()

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Busca Usuário (Username ou Email)
        user = UserModel.objects.filter(
            models.Q(username=username) | models.Q(email=username)
        ).first()
        if user and user.check_password(password):
            return user

        # Busca Empresa (Username, Email ou Registro)
        try:
            from Companies.models import CompanyModel
            company = CompanyModel.objects.filter(
                models.Q(username=username) | 
                models.Q(email=username) | 
                models.Q(registration_number=username)
            ).first()
            
            # Nota: se suas empresas ainda usam texto puro, mantenha o == 
            # Mas o padrão AbstractUser do seu model exige check_password
            if company and company.check_password(password):
                return company
        except Exception:
            pass

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            try:
                from Companies.models import CompanyModel
                return CompanyModel.objects.get(pk=user_id)
            except:
                return None

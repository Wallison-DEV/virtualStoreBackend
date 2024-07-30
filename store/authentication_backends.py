from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from Companies.models import CompanyModel

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        try:
            company = CompanyModel.objects.get(username=username)
            if company.password == password:
                return company
        except CompanyModel.DoesNotExist:
            pass
        
        try:
            company = CompanyModel.objects.get(registration_number=username)
            if company.password == password:
                return company
        except CompanyModel.DoesNotExist:
            pass
        
        try:
            company = CompanyModel.objects.get(email=username)
            if company.password == password:
                return company
        except CompanyModel.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            try:
                return CompanyModel.objects.get(pk=user_id)
            except CompanyModel.DoesNotExist:
                return None

from rest_framework import viewsets
from .models import CompanyModel
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
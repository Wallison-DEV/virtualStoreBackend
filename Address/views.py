# views.py
from rest_framework import viewsets
from .models import AddressModel
from .serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = AddressModel.objects.all()
    serializer_class = AddressSerializer

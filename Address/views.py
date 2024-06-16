# views.py
from rest_framework import viewsets
from .models import AddressModel
from .serializers import AddressModelSerializer

class AddressModelViewSet(viewsets.ModelViewSet):
    queryset = AddressModel.objects.all()
    serializer_class = AddressModelSerializer

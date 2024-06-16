from rest_framework import viewsets

from .models import CardModel
from .serializers import CardModelSerializer

class CardModelViewSet(viewsets.ModelViewSet):
    queryset = CardModel.objects.all()
    serializer_class = AddressModelSerializer

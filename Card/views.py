from rest_framework import viewsets

from .models import CardModel
from .serializers import CardSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = CardModel.objects.all()
    serializer_class = CardSerializer

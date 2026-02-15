from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import CardModel
from .serializers import CardSerializer

class CardViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet
                   ):
    queryset = CardModel.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CardModel.objects.filter(user=self.request.user).select_related('user')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

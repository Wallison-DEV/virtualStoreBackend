from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CardModel
from .serializers import CardSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = CardModel.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        if request.user.id != request.data.get('user_id'):
            return Response({'error': 'You are not authorized to create this card for another user'}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

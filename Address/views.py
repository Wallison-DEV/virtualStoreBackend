# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AddressModel
from .serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = AddressModel.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        if request.user.id != request.data.get('user_id'):
            return Response({'error': 'You are not authorized to create this address for another user'}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)
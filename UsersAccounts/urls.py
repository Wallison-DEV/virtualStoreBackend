from django.urls import path
from rest_framework_simplejwt.views import   TokenBlacklistView

from .views import CustomTokenObtainPairView, TokenValidateView, CustomTokenRefreshView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/validate/', TokenValidateView.as_view(), name='token_validate'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', TokenBlacklistView.as_view(), name='logout'),
]

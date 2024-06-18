from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Address.views import AddressViewSet
from Card.views import CardViewSet
from Orders.views import OrderViewSet
from Products.views import CategoryViewSet, ProductViewSet
from UsersAccounts.views import UserViewSet
from UsersAccounts import urls as UserUrls
from Companies.views import CompanyViewSet

router = DefaultRouter()
router.register(r'address', AddressViewSet)
router.register(r'card', CardViewSet)
router.register(r'order', OrderViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'user', UserViewSet)
router.register(r'company', CompanyViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('', include(UserUrls))
]

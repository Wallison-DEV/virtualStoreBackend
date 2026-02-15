from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from Address.views import AddressViewSet
from Card.views import CardViewSet
from Orders.views import OrderViewSet
from Products.views import ProductViewSet
from UsersAccounts.views import UserViewSet
from UsersAccounts import urls as UserUrls
from Companies.views import CompanyViewSet, CompanyProductLineViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'address', AddressViewSet, basename='address')
router.register(r'card', CardViewSet, basename='card')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'user', UserViewSet, basename='user')
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'product-lines', CompanyProductLineViewSet, basename='product-lines')
router.register(r'rating', RatingViewSet, basename='rating')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('', include(UserUrls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import include, path
from rest_framework import routers
from .views import AddressViewSet, ClientViewSet, CommandViewSet,ProductViewSet, ProviderViewSet
from e_commerce_app.views import ProductViewSet,ClientViewSet

router=routers.DefaultRouter()
router.register(r'products',ProductViewSet,basename='product')
router.register(r'clients',ClientViewSet,basename='client')
router.register(r'addresses',AddressViewSet,basename='address')
router.register(r'providers',ProviderViewSet,basename='provider')
router.register(r'commands',CommandViewSet,basename='command')
urlpatterns = [
    
    path('',include(router.urls)),
    path('max_min_price/', ProductViewSet.as_view({'get': 'max_min_price'}), name='max_min_price'),
    path(r'client_products', CommandViewSet.as_view({'get': 'client_products'}), name='client_products'),
    path('not_satisfied/',CommandViewSet.as_view({'get':'not_satisfied_clients'})
         , name='not_satisfied_clients'),
]

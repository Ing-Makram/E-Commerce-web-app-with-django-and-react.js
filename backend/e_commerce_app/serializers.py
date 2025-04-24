from rest_framework import serializers
from .models import Product,Client,Address,Provider,Command
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
class ProviderSerializer(serializers.ModelSerializer):
    address=AddressSerializer(read_only=True)
    class Meta:
        model = Provider
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    provider=ProviderSerializer()#read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    address=AddressSerializer(read_only=True)
    client_products=serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields='__all__'
        #fields = ('name','email','phone','typeClient')

class CommandSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    client=ClientSerializer(read_only=True)
    
    class Meta:
        model = Command
        fields = '__all__'
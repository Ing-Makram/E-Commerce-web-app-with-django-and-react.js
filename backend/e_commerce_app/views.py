from django.shortcuts import render
from .models import Address, Product, Client, Provider, Command
from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Max, Min
from django.utils import timezone
from .serializers import AddressSerializer, CommandSerializer, ProductSerializer, ClientSerializer, ProviderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['get'], detail=False)
    def in_stock(self, request):
        products = Product.objects.filter(stock__gt=0).order_by('label')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def out_of_stock(self, request):
        products = Product.objects.filter(stock=0).order_by('label')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(methods=['get'], detail=True)
    def get_products(self, request, pk=None):
        client = Client.objects.get(id=pk)
        products = client.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def command_product(self, request, pk=None):
        client = Client.objects.get(id=pk)
        product = Product.objects.get(id=request.data['product_id'])
        client.client_products.add(product)
        client.save()
        return Response({'message': f'Command of product {product.label} by the client {client.name} was accepted'})

    @action(methods=['delete'], detail=True)
    def remove_product(self, request, pk=None):
        client = Client.objects.get(id=pk)
        product = Product.objects.get(id=request.data['product_id'])
        client.products.remove(product)
        client.save()
        return Response({'message': 'Product removed from the client'})

    @action(methods=['get', 'post'], detail=True)
    def products(self, request, pk=None):
        if request.method == 'GET':
            return self.get_products(request, pk)
        elif request.method == 'POST':
            return self.add_product(request, pk)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def products2(self, request, pk=None):
        if request.method == 'GET':
            return self.get_products(request, pk)
        elif request.method == 'POST':
            return self.add_product(request, pk)
        elif request.method == 'DELETE':
            return self.remove_product(request, pk)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer    

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

    @action(detail=True, methods=['get'])
    def client_products(self, request):
        client_id = request.query_params.get('client_id', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if client_id and start_date and end_date:
            try:
                client = Client.objects.get(pk=client_id)
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            except (ValueError, Client.DoesNotExist):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            commands = Command.objects.filter(client=client, date_cmd__range=[start_date, end_date])
            product_ids = [command.product.id for command in commands]
            products = Product.objects.filter(id__in=product_ids, stock__gt=0).order_by('label')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def not_satisfied_clients(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if start_date and end_date:
            try:
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            commands = Command.objects.filter(date_cmd__range=[start_date, end_date])
            client_ids = [command.client.id for command in commands]
            clients = Client.objects.filter(id__in=client_ids, client_products__stock__lte=0).distinct().order_by('name')
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
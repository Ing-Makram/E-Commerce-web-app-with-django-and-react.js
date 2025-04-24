from django.db import models
from datetime import date
from django.utils import timezone



class ClientType(models.TextChoices):
    normal=('NORMAL','Normal Customer')
    loyal=('LOYAL','Loyal Customer')
    vip=('VIP','VIP Customer')
class Address(models.Model):
    houseNumber = models.PositiveSmallIntegerField(default=0)
    street = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    postalCode = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'address'
        ordering = ['country', 'city']
    def __str__(self):
        return f'id = {self.id}'
    


class User(models.Model):
    name = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['email']

    def __str__(self):
        return f'name={self.name}, email={self.email}, phone={self.phone}'


class Provider(User):
    site_url = models.URLField(default='')

    class Meta:
        db_table = 'providers'
        

    def __str__(self):
        # return f'name={self.name}, email={self.email}, phone={self.phone}, site_url={self.site_url}'
            return self.name


class Product(models.Model):
    # id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=100, default='')
    price = models.FloatField(default=0)
    stock = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='images/product_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    expirationDate = models.DateField(default=date(2023, 12, 31))
    fabricationDate = models.DateField(default=timezone.now)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'products'
        ordering = ['label', '-price']

    def __str__(self):
        return f'id={self.id}'

class Client(User):
    familyName = models.CharField(max_length=100, default='')
    typeClient = models.CharField(max_length=50, choices=[('LOYAL', 'Loyal Customer'), ('NORMAL', 'Normal Customer'),('VIP', 'Very Import Customer')], default='NORMAL')
    typeClient = models.CharField(max_length=50, choices=ClientType.choices, default=ClientType.normal)
    client_products = models.ManyToManyField(Product, through='Command', through_fields=('client', 'product'))

    class Meta:
        db_table = 'clients'
    def __str__(self):
        return f'id={self.id}'
    

class Command(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_cmd = models.DateField(default=timezone.now)
    quantity = models.PositiveSmallIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        db_table = 'commands'
        ordering = ['-date_cmd']
        verbose_name = 'Command table'
        verbose_name_plural = 'Command List'
        unique_together = [('client', 'product', 'date_cmd')]

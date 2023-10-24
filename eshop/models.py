from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True )
    name = models.CharField(max_length=90, null=True,blank=True)
    email = models.CharField(max_length=90, null=True,blank=True)

    def __str__(self):
        return self.name

class ComputerDetail(models.Model):

    Product_id = models.IntegerField()
    name = models.CharField(max_length=30)
    processor = models.CharField(max_length=90)
    image = models.ImageField(null=True, blank=True, upload_to='pics')
    ram = models.CharField(max_length=30)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):        
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(ComputerDetail, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=300, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    pincode = models.PositiveIntegerField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name

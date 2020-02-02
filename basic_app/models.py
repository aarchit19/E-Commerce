from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class CustProfileInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=240,unique=False,default=None)
    Phone = models.IntegerField(validators=[MinValueValidator(1000000000),
                                       MaxValueValidator(9999999999)],unique=True,default=None)
    Address=models.CharField(max_length=240,unique=False,default=None)
    Zipcode=models.IntegerField(validators=[MinValueValidator(100000),
                                       MaxValueValidator(999999)],unique=False,default=None)
    wallet_balance=models.BigIntegerField(default=0)


    def __str__(self):
        return self.user.username

class VendorProfileInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #additional
    Name = models.CharField(max_length=240,unique=False,default=None)
    Phone = models.IntegerField(validators=[MinValueValidator(1000000000),
                                       MaxValueValidator(9999999999)],unique=True,default=None)
    Address=models.CharField(max_length=240,unique=False,default=None)
    Shop_Name = models.CharField(max_length=240,unique=False,default=None)
    order_history=models.FileField(upload_to='order_file/',default=None)

    def __str__(self):
        return self.user.username

class SoldItem(models.Model):
    vendor=models.ForeignKey(VendorProfileInfo, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    picture=models.ImageField(upload_to='item_photo',blank=True)
    description=models.TextField(max_length=256)
    price=models.IntegerField(default=0)
    available_quantity=models.IntegerField(default=0)
    sold_quantity=models.IntegerField(default=0)

class PurchasedItem(models.Model):
    customer=models.ForeignKey(CustProfileInfo, on_delete=models.CASCADE)
    item=models.ForeignKey(SoldItem, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    order_complete=models.BooleanField(default=False)
    cost=models.BigIntegerField(default=0)

class CartItem(models.Model):
    customer=models.ForeignKey(CustProfileInfo, on_delete=models.CASCADE)
    item=models.ForeignKey(SoldItem, on_delete=models.CASCADE)
    requested_quantity=models.IntegerField(default=0)
    cost=models.BigIntegerField(default=0)

class WishList(models.Model):
    customer=models.ForeignKey(CustProfileInfo, on_delete=models.CASCADE)
    item=models.ForeignKey(SoldItem, on_delete=models.CASCADE)

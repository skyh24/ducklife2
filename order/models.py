# -*- coding: utf-8 -*-
from django.db import models
from product.models import Product

# Create your models here.

class Order(models.Model):
    id = models.CharField(max_length = 22, primary_key = True)
    openid = models.CharField(max_length = 64)
    name = models.CharField(max_length = 16)
    phone = models.CharField(max_length = 16)
    address = models.CharField(max_length = 64)
    price = models.DecimalField(max_digits = 10,
        decimal_places = 2)
    datetime = models.DateTimeField(auto_now_add = True)
    isPaid = models.BooleanField(default = False)
    isCancel = models.BooleanField(default = False)
    isDelivery = models.BooleanField(default = False)

class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    number = models.IntegerField(default = 0)
    send = models.CharField(max_length = 16)
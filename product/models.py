# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 32)
    datetime = models.DateTimeField(auto_now_add = True)

class Customer(models.Model):
    openid = models.CharField(max_length = 256)
    addrone = models.CharField(max_length = 256)
    addrtwo = models.CharField(max_length = 256)

class Product(models.Model):
    uid = models.CharField(max_length = 16, unique = True)
    name = models.CharField(max_length = 32)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10,
        decimal_places = 2)
    sell = models.IntegerField(default = 0)
    datetime = models.DateTimeField(auto_now_add = True)
    picture = models.ImageField(upload_to = 'products')
    category = models.ForeignKey(Category)

class Cart:
    def __init__(self):
        self.items = {}
        self.total = 0.0

    def add(self, product, number):
        number = int(number)
        if product.uid in self.items:
            self.items[product.uid] += number
            self.total += float(product.price) * number
        else:
            self.items[product.uid] = 0
            self.items[product.uid] += number
            self.total += float(product.price) * number

    def reduce(self, product):
        if product.uid in self.items:
            self.items[product.uid] -= 1
            self.total -= float(product.price)

    def cancel(self, product, number):
        number = int(number)
        if product.uid in self.items:
            self.total -= float(product.price) * number
            self.items.pop(product.uid)

    def empty(self):
        if len(self.items) == 0:
            return True
        return False

    def clear(self):
        self.items.clear()
        self.total = 0.0
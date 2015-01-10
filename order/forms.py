# -*- coding: utf-8 -*-
from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length = 16)
    phone = forms.CharField(max_length = 16)
    address = forms.CharField(max_length = 64)
    uid = forms.CharField(max_length = 16)
    price = forms.CharField(max_length = 16)
    number = forms.CharField(max_length = 16)
    send = forms.CharField(max_length = 16)
# -*- coding: utf-8 -*-
from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length = 32)
    description = forms.CharField(widget = forms.Textarea)
    price = forms.DecimalField(max_digits = 10,
        decimal_places = 2)
    picture = forms.ImageField()
    category = forms.CharField(max_length = 32)
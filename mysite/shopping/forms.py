"""forms.py"""
from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    """ProductForm"""

    class Meta:
        """Meta"""
        model = Products
        fields = ('code', 'name', 'price', 'description')

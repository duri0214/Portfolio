"""forms.py"""
from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    """ProductForm"""
    class Meta:
        """Meta"""
        model = Products
        fields = ('code', 'name', 'price', 'picture', 'description')

class UploadCSVForm(forms.Form):
    """ formのname 属性が 'file' になる """
    file = forms.FileField(required=True, label='')

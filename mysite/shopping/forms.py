"""forms.py"""
from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    """ ProductForm """
    class Meta:
        """Meta"""
        model = Products
        fields = ('code', 'name', 'price', 'picture', 'description')

class EditForm(forms.ModelForm):
    """ EditForm """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['readonly'] = 'readonly'
        self.fields['code'].widget.attrs['width'] = '10%'
        self.fields['name'].widget.attrs['width'] = '15%'
        self.fields['price'].widget.attrs['width'] = '10%'
        self.fields['description'].widget.attrs['width'] = '40%'
    class Meta:
        """Meta"""
        model = Products
        fields = ('code', 'name', 'price', 'description')

class UploadCSVForm(forms.Form):
    """ formのname 属性が 'file' になる """
    file = forms.FileField(required=True, label='')

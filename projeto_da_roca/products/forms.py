from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
#from django.core.exceptions import ValidationError
from .models import Product
from users.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'variety', 'expiration_days', 'price', 'stock_amount')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields['price'].widget.attrs['min'] = 0.01
        self.fields['stock_amount'].widget.attrs['min'] = 0
        self.fields['expiration_days'].widget.attrs['min'] = 0
        self.helper.layout = Layout(
            Field('name', placeholder='Nome'),
            Field('variety', placeholder='Variedade'),
            Field('expiration_days', placeholder='Dias de validade'),
            Field('price', placeholder='Preço por unidade'),
            Field('stock_amount', placeholder='Quantidade em estoque'),
            Submit('save', 'Salvar'),
        )

        
        

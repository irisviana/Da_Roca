from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Selecione uma categoria")

    class Meta:
        model = Product
        fields = ('category', 'name', 'variety',
                  'expiration_days', 'price', 'stock_amount')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields['price'].widget.attrs['min'] = 0.01
        self.fields['stock_amount'].widget.attrs['min'] = 0
        self.fields['expiration_days'].widget.attrs['min'] = 0
        self.helper.layout = Layout(
            Field('category', placeholder='Categoria'),
            Field('name', placeholder='Nome'),
            Field('variety', placeholder='Variedade'),
            Field('expiration_days', placeholder='Dias de validade'),
            Field('price', placeholder='Preço por unidade'),
            Field('stock_amount', placeholder='Quantidade em estoque'),
            Submit('save', 'Salvar'),
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('name', type='text', placeholder='Nome'),
            Submit('save', 'Cadastrar'),
        )

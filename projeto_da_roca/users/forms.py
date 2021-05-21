from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django.core.exceptions import ValidationError

from .models import User
from .models import Address
from .utils import validate_cpf


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)
    cpf = forms.CharField(min_length=14, max_length=14)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'cpf', 'email', 'password',
                  'confirm_password', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('first_name', placeholder='Nome'),
            Field('last_name', placeholder='Sobrenome'),
            Field('cpf', placeholder='CPF'),
            Field('phone_number', placeholder='Número de telefone'),
            Field('email', placeholder='E-mail'),
            Field('password', placeholder='Senha'),
            Field('confirm_password', placeholder='Confirmar senha'),
            Submit('save', 'Cadastrar'),

        )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = cpf.replace('.', '').replace('-', '')
            if validate_cpf(cpf):
                return cpf
        raise ValidationError('O CPF já está cadastrado')

    def clean(self):
        email = self.cleaned_data.get('email')
        cpf = self.cleaned_data.get('cpf')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('As senhas precisam ser idênticas')
        if User.objects.filter(email=email).exists():
            raise ValidationError('O e-mail já está cadastrado')
        if User.objects.filter(cpf=cpf).exists():
            raise ValidationError('O CPF já está cadastrado')
        return self.cleaned_data


class AddressForm(forms.ModelForm):
    STATE_CHOICES = (
        ('', 'Estado'),
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RO', 'Rondônio'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
        ('DF', 'Distrito Federal'),
    )
    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)

    class Meta:
        model = Address
        fields = ('zip_code', 'state', 'city', 'district', 'street', 'house_number')

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('zip_code', placeholder='CEP'),
            Field('city', placeholder='Cidade'),
            Field('street', placeholder='Rua'),
            Field('house_number', placeholder='Número da casa'),
            Field('district', placeholder='Bairro'),
            Field('state', placeholder='Estado'),
            Submit('save', 'Cadastrar'),

        )
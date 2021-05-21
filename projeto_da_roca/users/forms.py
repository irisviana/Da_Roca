from django.forms import ModelForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'cpf', 'email', 'password', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    def clean(self):
        email = self.cleaned_data.get('email')
        cpf = self.cleaned_data.get('cpf')
        if User.objects.filter(email=email).exists():
            raise ValidationError('O e-mail já está cadastrado')
        if User.objects.filter(cpf=cpf).exists():
            raise ValidationError('O CPF já está cadastrado')
        return self.cleaned_data

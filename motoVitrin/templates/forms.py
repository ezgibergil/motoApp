from django import forms
from motoVitrin.models import Sale
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['category', 'amount', 'sale_date', 'customer_name']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
        }

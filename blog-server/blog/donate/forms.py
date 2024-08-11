from django import forms
from donate.models import Donate

class DonateForm(forms.ModelForm):
    price = forms.IntegerField(min_value=50, widget=forms.NumberInput(attrs={
        'type': 'number',
        'placeholder': 'Введите сумму',
        'value': '50',
        'class': 'input_field',
    }))

    class Meta:
        model = Donate
        fields = ['price']


from django import forms


class CalcForm(forms.Form):
    first = forms.IntegerField(label="Первое число", max_value=1000, min_value=0,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    second = forms.IntegerField(label="Второе число", max_value=1000, min_value=0,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))

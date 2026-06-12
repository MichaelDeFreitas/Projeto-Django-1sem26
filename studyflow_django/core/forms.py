from django import forms

from .models import Perfil


class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        required=False,
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Seu nome'}),
    )
    last_name = forms.CharField(
        label='Sobrenome',
        required=False,
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Seu sobrenome'}),
    )
    email = forms.EmailField(
        label='E-mail',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'custom-input', 'placeholder': 'seuemail@exemplo.com'}),
    )

    class Meta:
        model = Perfil
        fields = ['meta_diaria']
        labels = {
            'meta_diaria': 'Meta diária de estudo em horas',
        }
        widgets = {
            'meta_diaria': forms.NumberInput(
                attrs={
                    'class': 'custom-input',
                    'min': 1,
                    'max': 24,
                    'placeholder': 'Ex: 4',
                }
            )
        }

    def clean_meta_diaria(self):
        meta = self.cleaned_data.get('meta_diaria')

        if meta is None:
            raise forms.ValidationError('Informe sua meta diária.')

        if meta < 1 or meta > 24:
            raise forms.ValidationError('A meta deve estar entre 1 e 24 horas.')

        return meta

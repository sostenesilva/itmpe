from django import forms
from .models import Db_Criterios, Db_Avaliacao, Email_group

class Criterios_form (forms.ModelForm):
    class Meta:
        model = Db_Criterios
        fields = ('item','criterio','dimensao','periodicidade')

        widgets = {
            'item': forms.TextInput(attrs={'class':'form-control'}),
            'criterio': forms.Textarea(attrs={'class':'form-control','rows':'5'}),
            'dimensao': forms.Select(attrs={'class':'form-control'}),
            'periodicidade': forms.Select(attrs={'class':'form-control'}),
        }

class Avaliacao_form (forms.ModelForm):
    class Meta:
        model = Db_Avaliacao
        fields = ('criterio','responsavel', 'data_limite','status')

        widgets = {
            'criterio': forms.Select(attrs={'class':'form-control'}),
            'responsavel': forms.Select(attrs={'class':'form-control'}),
            'data_limite': forms.DateInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }

class Email_group_form (forms.ModelForm):
    class Meta:
        model = Email_group
        fields = ('group','email_group')

        widgets = {
            'group': forms.Select(attrs={'class':'form-control form-sm'}),
            'email_group': forms.EmailInput(attrs={'class':'form-control form-sm'}),
        }
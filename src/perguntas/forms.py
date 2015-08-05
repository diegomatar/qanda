from django import forms
from django.forms import ModelForm

from .models import Pergunta, Resposta, Tag


class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['titulo', 'descricao', 'tags']
        
        

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['resposta',]
        
        
        
        
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nome',]
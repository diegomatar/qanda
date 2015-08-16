from django import forms
from django_select2 import AutoModelSelect2TagField

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from .models import Pergunta, Resposta, Tag



class TagField(AutoModelSelect2TagField):
    queryset = Tag.objects
    search_fields = ['nome__icontains', ]

    def get_model_field_values(self, value):
        
        return {'nome': value, 'slug':slugify(value)}


class PerguntaForm(forms.ModelForm):
    titulo = forms.CharField()
    descricao = forms.CharField(widget=forms.Textarea)
    tags = TagField()
    
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
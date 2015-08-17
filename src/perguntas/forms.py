#!/usr/bin/env python
# -*- coding: utf-8 -*-


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Field, Button, Div
from django_select2 import AutoModelSelect2TagField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from django import forms
from django.core.urlresolvers import reverse
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
    titulo = forms.CharField(label="Pergunta")
    descricao = forms.CharField(widget=SummernoteWidget(), label="Detalhes", required=False)
    tags = TagField(label="Tópicos")
    
    class Meta:
        model = Pergunta
        fields = ['titulo', 'descricao', 'tags']
        
    def __init__(self, *args, **kwargs):
        super(PerguntaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'perguntar'
        self.helper.form_class = 'perguntar'
        self.helper.form_method = 'post'
        self.helper.form_action = 'perguntar'
        
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'O que deseja saber hoje {{ user.first_name }}?',
            ),
            'titulo',
            HTML("""
                <p>Se desejar, escreva mais detalhes sobre o que deseja saber:</p>
            """),
            'descricao',
            'tags',
            Div(
                Submit('submit', 'Enviar Pergunta >', css_class='btn-info btn-lg'),
                css_class='col-lg-offset-3 col-lg-9',
            )
        )
             

class RespostaForm(forms.ModelForm):
    resposta = forms.CharField(widget=SummernoteInplaceWidget(), label="Resposta", required=True)
    
    class Meta:
        model = Resposta
        fields = ['resposta',]
        
    def __init__(self, *args, **kwargs):
        super(RespostaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'responder'
        self.helper.form_class = 'responder'
        self.helper.form_method = 'post'
        
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
     
            HTML("""
                <p>Seja sempre respeitoso e claro em suas respostas</p>
            """),
            'resposta',
            Div(
                Submit('submit', 'Enviar Resposta >', css_class='btn-info btn-lg'),
                css_class='col-lg-offset-3 col-lg-9',
            )
        )
        
        
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nome',]
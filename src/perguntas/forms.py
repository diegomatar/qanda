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

from .models import Pergunta, Resposta, Tag, Comment



class TagField(AutoModelSelect2TagField):
    queryset = Tag.objects
    search_fields = ['nome__icontains', ]

    

    def get_model_field_values(self, value):
        
        return {'nome': value, 'slug':slugify(value)}


class PerguntaForm(forms.ModelForm):
    titulo = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Qual é sua pergunta?'}))
    descricao = forms.CharField(widget=SummernoteInplaceWidget(), label=" ", required=False)
    tags = TagField(label=" ")
    
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
        

        self.helper.layout = Layout(
            'titulo',
            HTML("""
            <div id="collapseQsts">
            </div>
            <div id='newquestion'><button class="btn btn-warning" type="button">Minha Pergunta e Nova</button></div>
            """),
            HTML("""
                <div id="collapseDetails">
                <p class="sm-title close-to-next-line">Se desejar, escreva mais detalhes sobre o que deseja saber:</p>
            """),
            'descricao',
            HTML("""
                <p class="sm-title close-to-next-line">Quais os assuntos desta perguta?</p>
            """),
            'tags',
            Div(
                Submit('submit', 'Enviar Pergunta >', css_class='btn-warning btn-lg'),
                css_class='col-lg-offset-3 col-lg-9',
            ),
            HTML("""
            </div>
            """),
        )
             

class RespostaForm(forms.ModelForm):
    resposta = forms.CharField(widget=SummernoteInplaceWidget(), label="", required=True)
    
    class Meta:
        model = Resposta
        fields = ['resposta',]
        
    def __init__(self, *args, **kwargs):
        super(RespostaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'responder'
        self.helper.form_class = 'responder'
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            'resposta',
            Div(
                HTML("""
                <p class="info-text">Seja respeitoso e claro em suas respostas.</p>
            """),
                css_class='col-lg-8',
            ),
            Div(
                Submit('submit', 'Enviar Resposta', css_class='btn-warning'),
                css_class='col-lg-2',
            ),
        )
        
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nome',]
        
        
        
class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label="Comentário", required=True)
    
    
    class Meta:
        model = Comment
        fields = ['comment',]
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'comentar'
        self.helper.form_class = 'comentar'
        self.helper.form_method = 'post'
        
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
     
            HTML("""
                <p>Seja sempre respeitoso e claro em seus comentarios</p>
            """),
            'comment',
            Div(
                Submit('submit', 'Enviar Comentario >', css_class='btn-info btn-lg'),
                css_class='col-lg-offset-3 col-lg-9',
            )
        )
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
    titulo = forms.CharField(max_length=200, label="", widget=forms.TextInput(attrs={'placeholder': 'Exemplo: Qual a diferença entre um Deputado e um Senador?...'}))
    descricao = forms.CharField(max_length=800, widget=SummernoteInplaceWidget(), label="", required=False)
    tags = TagField(label="")
    
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
            HTML("""
                <p class="lead blog-description close-to-next-line"><b>1.</b> Escreva sua pergunta:</p>
            """),
            'titulo',
            HTML("""
            <div id="collapseQsts">
            {% include "perguntas/sugest_question.html" %}
            </div>
            """),
            HTML("""
                <p class="lead blog-description close-to-next-line"><b>2.</b> (opcional) escreva mais detalhes sobre o que deseja saber:</p>
            """),
            'descricao',
            HTML("""
                <p class="lead blog-description close-to-next-line"><b>3.</b> Escolha quais os temas desta perguta?</p>
                <p class="info-text">
                    Clique nos temas sugeridos ou use "enter" para criar um novo tema.
                    <br>
                    Exemplo: <i>Tecnologia, Faculdade, Governo, etc.</i> - limite de 6 temas
                </p>
            """),
            'tags',
            Div(
                Submit('enviar-pergunta', 'Enviar Pergunta', css_class='btn-warning btn-lg btn-block'),
                css_class='col-lg-offset-3 col-lg-6',
            ),
        )
        

class EditarPerguntaForm(forms.ModelForm):
    titulo = forms.CharField(max_length=200, label="", widget=forms.TextInput(attrs={'placeholder': 'Qual é sua pergunta?'}))
    descricao = forms.CharField(max_length=800, widget=SummernoteInplaceWidget(), label=" ", required=False)
    tags = TagField(label=" ")
    
    class Meta:
        model = Pergunta
        fields = ['titulo', 'descricao', 'tags']
        
    def __init__(self, *args, **kwargs):
        super(EditarPerguntaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'perguntar'
        self.helper.form_class = 'editar_pergunta'
        self.helper.form_method = 'post'
        

        self.helper.layout = Layout(
            'titulo',
            'descricao',
            HTML("""
                <p class="sm-title close-to-next-line">Quais os assuntos desta perguta?</p>
            """),
            'tags',
            Div(
                Submit('submit', 'Alterar Pergunta >', css_class='btn-warning btn-lg'),
                css_class='col-lg-offset-3 col-lg-9',
            ),
        )

    
             

class RespostaForm(forms.ModelForm):
    resposta = forms.CharField(max_length=2000, widget=SummernoteInplaceWidget(), label="", required=True)
    
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
            HTML("""
                <div class="row">
            """),
            Div(
                HTML("""
                <p class="info-text">Seja respeitoso e claro em suas respostas.</p>
            """),
                css_class='col-lg-8',
            ),
            Div(
                Submit('enviar-resposta', 'Enviar Resposta', css_class='btn-warning'),
                css_class='col-lg-2',
            ),
            HTML("""
                </div>
            """),
        )
        
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nome',]
        
        
        
class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=800, widget=forms.Textarea, label="Comentário", required=True)
    
    
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
                Submit('enviar-pergunta', 'Enviar Comentario', css_class='btn-warning btn-lg btn-block'),
                css_class='col-lg-offset-3 col-lg-6',
            ),
        )
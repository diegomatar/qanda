#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Field, Button, Div
from django_select2 import AutoModelSelect2TagField

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from perguntas.forms import TagField
from .models import UserProfile



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nome', required=True)
    last_name = forms.CharField(max_length=30, label='Sobrenome', required=True)
    

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        perfil = UserProfile(user=user)
        slug = str(user.first_name) +' '+ str(user.last_name)
        slug = slugify(slug)
        
        # If slug is already taken, add a random number at the end of it
        try:
            UserProfile.objects.get(slug=slug)
            slug = slug + str(randint(0,100))
        except:
            pass
        
        perfil.slug = slug
        perfil.save()

        
class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(max_length=30, label="Nome", required=True)
    last_name = forms.CharField(max_length=30, label="Sobrenome", required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            
        )
        

class EditProfileForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea, label="Sobre você", required=False, max_length = 150)

    class Meta:
        model = UserProfile
        fields = ('about',)
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Field('about', rows="3"),
        )


class EditProfilePictureForm(forms.ModelForm):
    picture = forms.ImageField(label="", required=False)
    
    class Meta:
        model = UserProfile
        fields = ('picture',)
        
    def __init__(self, *args, **kwargs):
        super(EditProfilePictureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'picture',
        )

        

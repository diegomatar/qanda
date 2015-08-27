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
        self.helper.layout = Layout(
            
        )
        
        
        

class EditProfileForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea, label="Sobre você", required=False)
    twitter = forms.URLField(label="Twitter", required=False)
    facebook = forms.URLField(label="Facebook", required=False)
    linkedin = forms.URLField(label="Linkedin", required=False)
    picture = forms.ImageField(label="Alterar Foto de Perfil", required=False)
    interests = TagField(label="Tópicos você tem interesse:", required=False)
    knows_about = TagField(label="Temas que você conhece bem:", required=False)
    
    class Meta:
        model = UserProfile
        fields = ('interests', 'knows_about', 'about', 'twitter', 'facebook', 'linkedin', 'picture')
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'interests',
            'knows_about',
            'about',
            'twitter',
            'facebook',
            'linkedin',
            HTML("""
                <div class='row'>
                <div class='col-md-6'>
            """),
            'picture',
            HTML("""
                </div>
                <div class='col-md-6'>
                <p><b>Foto atual:</b> <img class='profile-pic' src='{{ user.profile_image_url }}'></p>
                </div>
                </div>
            """),
        )


        

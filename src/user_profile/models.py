#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User

from perguntas.models import Pergunta, Resposta, Tag

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(verbose_name='email')
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Nome')
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Sobrenome')
    about = models.TextField(max_length=500, blank=True, null=True, verbose_name='Sobre')
    twitter = models.CharField(max_length=200, blank=True, null=True, verbose_name='Twitter')
    facebook = models.URLField(max_length=200, blank=True, null=True, verbose_name='Facebook')
    linkedin = models.URLField(max_length=200, blank=True, null=True, verbose_name='Linked In')
    picture = models.ImageField(upload_to='profile_pictures', verbose_name='Imagem de Perfil')
    points = models.IntegerField(default=0)
    perg_upvotes = models.ManyToManyField(Pergunta, related_name='perg_upvotes')
    perg_downvotes = models.ManyToManyField(Pergunta, related_name='perg_downvotes')
    resp_upvotes = models.ManyToManyField(Resposta, related_name='resp_upvotes')
    resp_downvotes = models.ManyToManyField(Resposta, related_name='resp_downvotes')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def perguntas(self):
        pergs = Pergunt.objects.filter(autor=self.user)
        return pergs
    
    def num_pergs(self):
        pergs = Pergunt.objects.filter(autor=self.user)
        return len(pergs)
    
    def respostas(self):
        resp = Resposta.objects.filter(autor=self.user)
        return resp
    
    def num_respostas(self):
        resp = Resposta.objects.filter(autor=self.user)
        return len(resp)
        
        
    def __unicode__(self):
        return self.user.email
    
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from allauth.socialaccount.models import SocialAccount

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from perguntas.models import Pergunta, Resposta


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(default="slug")
    about = models.TextField(max_length=500, blank=True, null=True, verbose_name='Sobre')
    twitter = models.CharField(max_length=200, blank=True, null=True, verbose_name='Twitter')
    facebook = models.URLField(max_length=200, blank=True, null=True, verbose_name='Facebook')
    linkedin = models.URLField(max_length=200, blank=True, null=True, verbose_name='Linked In')
    picture = models.ImageField(upload_to='profile_pictures', verbose_name='Imagem de Perfil', blank=True, null=True)
    points = models.IntegerField(default=0)
    perg_upvotes = models.ManyToManyField('perguntas.Pergunta', related_name='perg_upvotes')
    perg_downvotes = models.ManyToManyField('perguntas.Pergunta', related_name='perg_downvotes')
    resp_upvotes = models.ManyToManyField('perguntas.Resposta', related_name='resp_upvotes')
    resp_downvotes = models.ManyToManyField('perguntas.Resposta', related_name='resp_downvotes')
    follow_users = models.ManyToManyField(User, related_name='follows')
    follow_questions = models.ManyToManyField('perguntas.Pergunta', related_name='follow_questions')
    follow_topics = models.ManyToManyField('perguntas.Tag', related_name='follow_topics')
    interests = models.ManyToManyField('perguntas.Tag', related_name='interests')
    knows_about = models.ManyToManyField('perguntas.Tag', related_name='knows_about')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def profile_image_url(self):
        if self.picture:
            return "/media/" + str(self.picture)
        
        else:
            fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
         
            if len(fb_uid):
                return "http://graph.facebook.com/{}/picture".format(fb_uid[0].uid)+"?type=large"
         
            return "http://www.gravatar.com/avatar/{}".format(hashlib.md5(self.user.email).hexdigest())+"?s=200"
    
    def name(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def perguntas(self):
        pergs = Pergunta.objects.filter(autor=self.user)
        return pergs
    
    def num_pergs(self):
        pergs = Pergunta.objects.filter(autor=self.user)
        return len(pergs)
    
    def respostas(self):
        resp = Resposta.objects.filter(autor=self.user)
        return resp
    
    def num_respostas(self):
        resp = Resposta.objects.filter(autor=self.user)
        return len(resp)
    
    def followers_num(self):
        followers = self.user.follows.all()
        return len(followers)
        
        
    def __unicode__(self):
        return self.user.email
    
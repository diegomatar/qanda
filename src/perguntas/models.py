#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError


# Create your models here.


class Tag(models.Model):
    nome = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(unique=True)
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='tag')
    
    def __unicode__(self):
        return self.nome
    
    def get_absolute_url(self, ):
        return reverse('tag', args=[self.slug])
    
    def perguntas(self,):
        perg = self.pergunta_set.all()
        return perg
    
    def num_perguntas(self, ):
        perg = self.pergunta_set.all()
        return len(perg)
    
    
    def followers_num(self):
        followers = self.follow_topics.all()
        return len(followers)
    
    
    def followed(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self in profile.follow_topics.all():
            return 1
        else:
            return 0
    
    
    
    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        
        try: #create a new Tag object
            super(Tag, self).save(*args, **kwargs)
        
        except IntegrityError: # in case of errors, replace the instance by the existing one
            existing_tag = Tag.objects.get(slug=self.slug)
            self.pk = existing_tag.pk
            # Now pk != 0 and objects should be updated:
            self.save()



class Pergunta(models.Model):
    autor = models.ForeignKey(User)
    data = models.DateField(default=datetime.now)
    titulo = models.CharField(max_length=300, verbose_name='Título')
    slug = models.SlugField(unique=True)
    descricao = models.TextField(verbose_name='Descrição', max_length=5000, blank=True, null=True)
    views = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    asked_count = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='pergunta')
    
    def __unicode__(self):
        return self.titulo
    
    def get_absolute_url(self, ):
        return reverse('pergunta', args=[self.slug])
    
    def num_respostas(self,):
        resp = self.resposta_set.all()
        return len(resp)
    
    def respostas(self,):
        resp = self.resposta_set.all()
        return resp
    
    def upvoted(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self in profile.perg_upvotes.all():
            return 1
        else:
            return 0
    
    def downvoted(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self in profile.perg_downvotes.all():
            return 1
        else:
            return 0
        
    
    
    def followed(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self in profile.follow_questions.all():
            return 1
        else:
            return 0
        
    def followers_num(self):
        followers = self.follow_questions.all()
        return len(followers)
    


class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta)
    autor = models.ForeignKey(User)
    data = models.DateField(default=datetime.now)
    resposta = models.TextField(max_length=5000)
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='resposta')
    
    def __unicode__(self):
        return 'Por %s em %s' % (self.autor, self.data)
    
    
    def upvoted(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self in profile.resp_upvotes.all():
            return 1
        else:
            return 0
        
    def downvoted(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self in profile.resp_downvotes.all():
            return 1
        else:
            return 0
        
    def comment_num(self, ):
        comments = self.comment_set.all()
        num_comments = len(comments)
        return num_comments
    
        

class Comment(models.Model):
    answer = models.ForeignKey(Resposta)
    autor = models.ForeignKey(User)
    data = models.DateField(default=datetime.now)
    comment = models.TextField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='comment')
    
    def __unicode__(self):
        return 'Por %s em %s' % (self.autor, self.data)
        
        
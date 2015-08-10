#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from user_profile.models import UserProfile
from perguntas.models import Pergunta, Resposta, Tag

unread_status = (
    (1, 'unread'),
    (0, 'read'),
)

vote = (
    (1, 'like'), #like
    (0, 'unlike'), #unlike
)

class NotiAnswer(models.Model):
    to_user = models.ForeignKey(User, related_name='anotif_to_user')
    from_user = models.ForeignKey(User, related_name='anotif_from_user')
    unread = models.IntegerField(default=1, choices=unread_status)
    question = models.ForeignKey(Pergunta, related_name='question')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    kind = models.CharField(max_length=50, default='answer')
    
    @property
    def note(self,):
        return self.from_user.first_name + " respondeu sua pergunta."
    
    @property
    def note_full(self, ):
        return self.from_user.first_name + " respondeu sua pergunta: " + self.question.titulo + ". Veja a resposta aqui." 
    
    def __unicode__(self):
        return unicode(self.to_user)
    

class NotiVote(models.Model):
    to_user = models.ForeignKey(User, related_name='vnotif_to_user')
    from_user = models.ForeignKey(User, related_name='vnotif_from_user')
    unread = models.IntegerField(default=1, choices=unread_status)
    vote = models.IntegerField(default=1, choices=vote)
    question = models.ForeignKey(Pergunta, blank=True, null=True)
    answer = models.ForeignKey(Resposta, blank=True, null=True, related_name='answer')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    kind = models.CharField(max_length=50, default='vote')
    
    @property
    def note(self, ):
        if self.question:
            if self.vote:
                return self.from_user.first_name + " gostou de sua pergunta!"
            else:
                return self.from_user.first_name + " nao gostou da sua pergunta..."
            
        elif self.answer:
            if self.vote:
                return self.from_user.first_name + " gostou de sua resposta!"
            else:
                return self.from_user.first_name + " nao gostou de sua resposta..."
        else:
            return "Que tal melhorar o perfil seu clicando aqui!"

    @property
    def note_full(self, ):
        if self.question:
            if self.vote:
                return self.from_user.first_name + " gostou de sua pergunta: " + self.question.titulo
            else:
                return self.from_user.first_name + " nao gostou de sua pergunta: " + self.question.titulo
        elif self.answer:
            if self.vote:
                return self.from_user.first_name + " gostou de sua resposta: " + self.answer.resposta
            else:
                return self.from_user.first_name + " nao gostou de sua resposta " + self.answer.resposta
        else:
            return "Que tal melhorar o perfil seu clicando aqui!"
    
    def __unicode__(self):
        return unicode(self.to_user)


'''
 Actions that will create a new notification:
 - Someone answered your question
 - Someone voted in your answer
 - Someone voted in your question
 - Unread notifications will be displaied on page reload
 '''
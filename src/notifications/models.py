#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 Actions that will create a new notification:
 - Someone answered your question
 - Someone commented in your answer
 - Someone voted in your answer
 - Someone voted in your question
 - Someone starts following you
 - Someone requests you to ask a question
 '''

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from user_profile.models import UserProfile
from perguntas.models import Pergunta, Resposta, Tag, Comment

unread_status = (
    (1, 'unread'),
    (0, 'read'),
)

vote = (
    (1, 'like'), #like
    (0, 'unlike'), #unlike
)


class UserMessagesSet(models.Model):
    new_follower = models.BooleanField()
    follow_activities = models.BooleanField()
    answer_question = models.BooleanField()
    question_in_tag =  models.BooleanField()
    ask_answer =  models.BooleanField()
    new_comment =  models.BooleanField()
    new_vote =  models.BooleanField()
    email_summary_day =  models.BooleanField()
    email_summary_week =  models.BooleanField()
    


class NotiAnswer(models.Model):
    to_user = models.ForeignKey(User, related_name='anotif_to_user')
    from_user = models.ForeignKey(User, related_name='anotif_from_user')
    unread = models.IntegerField(default=1, choices=unread_status)
    question = models.ForeignKey(Pergunta, related_name='anotif_question')
    answer = models.ForeignKey(Resposta, related_name='anotif_answer', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    kind = models.CharField(max_length=50, default='answer')
    
    @property
    def icon(self,):
        return '<i class="fa fa-pencil fa-2x"></i>'
    
    @property
    def note(self,):
        return "respondeu a pergunta:"
    
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
    def icon(self, ):
        if self.question:
            if self.vote:
                return '<i class="fa fa-thumbs-o-up fa-2x"></i>'
            else:
                return '<i class="fa fa-thumbs-o-down fa-2x"></i>'
            
        elif self.answer:
            if self.vote:
                return '<i class="fa fa-thumbs-o-up fa-2x"></i>'
            else:
                return '<i class="fa fa-thumbs-o-down fa-2x"></i>'
        
    
    @property
    def note(self, ):
        if self.question:
            if self.vote:
                return "gostou de sua pergunta:"
            else:
                return "nao gostou de sua pergunta:"
            
        elif self.answer:
            if self.vote:
                return "gostou de sua resposta para:"
            else:
                return 'não gostou de sua resposta para:'
        else:
            return "Que tal melhorar o perfil seu clicando aqui!"

    @property
    def item(self, ):
        if self.question:
            return 'question'
        elif self.answer:
            return 'answer'
    
    def __unicode__(self):
        return unicode(self.to_user)



class NotiFollow(models.Model):
    to_user = models.ForeignKey(User, related_name='fnotif_to_user')
    from_user = models.ForeignKey(User, related_name='fnotif_from_user')
    unread = models.IntegerField(default=1, choices=unread_status)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    kind = models.CharField(max_length=50, default='follow')
    
    @property
    def icon(self,):
        return '<i class="fa fa-user-plus fa-2x"></i>'
    
    @property
    def note(self,):
        return "comecou a seguir voce!"
    
    @property
    def note_full(self, ):
         return self.from_user.first_name + " comecou a seguir voce!"
    
    def __unicode__(self):
        return unicode(self.to_user)
    

class NotiComment(models.Model):
    to_user = models.ForeignKey(User, related_name='cnotif_to_user')
    from_user = models.ForeignKey(User, related_name='cnotif_from_user')
    answer = models.ForeignKey(Resposta)
    comment = models.ForeignKey(Comment, blank=True, null=True)
    unread = models.IntegerField(default=1, choices=unread_status)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    kind = models.CharField(max_length=50, default='comment')

    @property
    def icon(self,):
        return '<i class="fa fa-commenting-o fa-2x"></i>'

    @property
    def note(self,):
        return "comentou sua resposta:"
    
    @property
    def note_full(self, ):
         return self.from_user.first_name + " comentou sua resposta."
    
    def __unicode__(self):
        return unicode(self.to_user)
    
    

class NotiAsk(models.Model):
    to_user = models.ForeignKey(User, related_name='asknotif_to_user')
    from_user = models.ForeignKey(User, related_name='asknotif_from_user', blank=True, null=True)
    question = models.ForeignKey(Pergunta)
    unread = models.IntegerField(default=1, choices=unread_status)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    kind = models.CharField(max_length=50, default='ask_to_answer')

    def __unicode__(self):
        return unicode(self.to_user)
    
    @property
    def note(self,):
        return "pediu que você responda a pergunta:"
    
    @property
    def icon(self,):
        return '<i class="fa fa-university fa-2x"></i>'
    

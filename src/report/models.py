#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


from perguntas.models import Pergunta, Resposta, Comment
from user_profile.models import UserProfile

# Create your models here.

REPORT_KIND = (
    (1, "É irritante ou desinteressante"),
    (2, "Tem relação comigo e não gostei"),
    (3, "Acho que não deveria estar no QANDA"),
    (4, "É spam ou propaganda"),
)

STATUS = (
    (1, 'new'),
    (0, 'checked'),
)

class Question_Report(models.Model):
    question = models.ForeignKey(Pergunta)
    from_users = models.ManyToManyField(User)
    kind = models.IntegerField(choices=REPORT_KIND)
    status = models.IntegerField(choices=STATUS, default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='question_report')
    
    def report_num(self, ):
        return len(self.from_users)
    
    def __unicode__(self):
        return 'Pergunta: %s ' % self.question.titulo
    
    

class Answer_Report(models.Model):
    answer = models.ForeignKey(Resposta)
    from_users = models.ManyToManyField(User)
    kind = models.IntegerField(choices=REPORT_KIND)
    status = models.IntegerField(choices=STATUS, default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='answer_report')
    
    def report_num(self, ):
        return len(self.from_users)
    
    def __unicode__(self):
        return 'Pergunta: %s ' % self.answer.resposta
    
    
    

class Comment_Report(models.Model):
    comment = models.ForeignKey(Comment)
    from_users = models.ManyToManyField(User)
    kind = models.IntegerField(choices=REPORT_KIND)
    status = models.IntegerField(choices=STATUS, default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='comment_report')
    
    def report_num(self, ):
        return len(self.from_users)
    
    def __unicode__(self):
        return 'Pergunta: %s ' % self.comment.comment
    
    
    


class Profile_Report(models.Model):
    profile = models.ForeignKey(UserProfile)
    from_users = models.ManyToManyField(User)
    kind = models.IntegerField(choices=REPORT_KIND)
    status = models.IntegerField(choices=STATUS, default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    classe = models.CharField(max_length=100, default='profile_report')
    
    def report_num(self, ):
        return len(self.from_users)
    
    def __unicode__(self):
        return 'Pergunta: %s ' % self.profile.name
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from allauth.socialaccount.models import SocialAccount
from random import randint

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from perguntas.models import Pergunta, Resposta

USER_ROLES = (
    ('regular', 'regular'),
    ('editor', 'editor'),
    ('admin', 'admin'),
)



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(default="slug")
    about = models.TextField(max_length=500, blank=True, null=True, verbose_name='Sobre')
    twitter = models.CharField(max_length=200, blank=True, null=True, verbose_name='Twitter')
    facebook = models.URLField(max_length=200, blank=True, null=True, verbose_name='Facebook')
    google = models.URLField(max_length=200, blank=True, null=True, verbose_name='Google')
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
    user_role = models.CharField(choices=USER_ROLES, default='regular', max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def profile_image_url(self):
        if self.picture:
            return "/media/" + str(self.picture)
        
        else:
            fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
            twitter_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='twitter')
            google_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
            
            if len(fb_uid):
                return fb_uid[0].get_avatar_url()
                #return "http://graph.facebook.com/{}/picture".format(fb_uid[0].uid)+"?type=large"
            
            elif len(twitter_uid):
                #url = twitter_uid.extra_data['profile_image_url']
                return twitter_uid[0].get_avatar_url()
            
            elif len(google_uid):
                return google_uid[0].get_avatar_url()
            
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
    
    def reputation(self):
        resp = Resposta.objects.filter(autor=self.user)
        reputation = 0
        for rsp in resp:
            reputation += rsp.votes
        return reputation
    
    
    def followed(self, user):
        try:
            profile = user.userprofile
        except:
            return 0
        if self.user in profile.follow_users.all():
            return 1
        else:
            return 0
        
        
    def __unicode__(self):
        return self.user.email
    
    
    def save(self, *args, **kwargs):
        slug = str(self.user.first_name) +' '+ str(self.user.last_name)
        slug = slugify(slug)
        print slug
        existent_slug = UserProfile.objects.filter(slug=slug)
        
        if len(existent_slug): #checks if slug exists, if it does add a random num to the end of it
            self.slug = slug + '-' + str(randint(0,100))
        
        else: # saves slug as it is
            self.slug = slug
        
        super(UserProfile, self).save(*args, **kwargs)
            
            


class UserBio(models.Model):
    user = models.ForeignKey(User)
    tag = models.ForeignKey('perguntas.Tag')
    bio = models.CharField(max_length=200, verbose_name='Sobre')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return self.bio
    
    
    

    
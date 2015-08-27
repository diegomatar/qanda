#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'num_perg', 'num_resp', 'p_upvotes', 'p_downvotes', 'r_upvotes', 'r_downvotes']
    search_fields = ['user__email', 'user_userbame', 'autor', 'tags__nome']
    list_filter = ['points', 'perg_upvotes', 'perg_downvotes', 'resp_upvotes', 'resp_downvotes']
    readonly_fields = ['timestamp', 'updated', 'points', 'num_perg', 'num_resp', 'perg_upvotes', 'perg_downvotes', 'resp_upvotes', 'resp_downvotes']
    
    class Meta:
        model = UserProfile
        
    def email(self, obj):
        email = obj.user.email
        return email
    
    def first_name(self, obj):
        first_name = obj.user.first_name
        return first_name
        
    def num_resp(self, obj):
        resp = []
        for i in obj.user.resposta_set.all():
            resp.append(i)
        return len(resp)
    
    def num_perg(self, obj):
        perg = []
        for i in obj.user.pergunta_set.all():
            perg.append(i)
        return len(perg)
    
    def p_upvotes(self, obj):
        perg = []
        for i in obj.perg_upvotes.all():
            perg.append(i)
        return len(perg)
    
    def p_downvotes(self, obj):
        perg = []
        for i in obj.perg_downvotes.all():
            perg.append(i)
        return len(perg)
    
    def r_upvotes(self, obj):
        resp = []
        for i in obj.resp_upvotes.all():
            resp.append(i)
        return len(resp)
    
    def r_downvotes(self, obj):
        resp = []
        for i in obj.resp_downvotes.all():
            resp.append(i)
        return len(resp)
        
    
admin.site.register(UserProfile, UserProfileAdmin)
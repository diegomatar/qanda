#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Pergunta, Resposta, Tag


# Register your models here.
class RespostaInline(admin.TabularInline):
    extra = 0
    model = Resposta
    readonly_fields = ['votes']


class PerguntaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tags_list','data', 'autor', 'num_resp', 'views', 'votes', 'live_link']
    inlines = [RespostaInline]
    search_fields = ['titulo', 'descricao', 'autor', 'tags__nome']
    list_filter = ['autor', 'data', 'tags__nome']
    prepopulated_fields = {"slug": ("titulo", )}
    readonly_fields = ['live_link', 'timestamp', 'updated', 'views', 'votes']
    
    class Meta:
        model = Pergunta
            
    def tags_list(self, obj):
        tgs = []
        for i in obj.tags.all():
            tgs.append(i.nome)
        return ", ".join(tgs)
        
    def num_resp(self, obj):
        resp = []
        for i in obj.resposta_set.all():
            resp.append(i)
        return len(resp)
    
    def live_link(self, obj):
        link = "<a href='/pergunta/"+obj.slug+"'/>"+"Ver Pergunta"+"</a>"
        return link
    
    live_link.allow_tags = True
    
    
admin.site.register(Pergunta, PerguntaAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'views', 'num_perg', 'num_resp']
    prepopulated_fields = {"slug": ("nome", )}
    readonly_fields = ['views', 'timestamp', 'updated', 'num_perg', 'num_resp']
    
    class Meta:
        model = Tag
        
    def num_perg(self, obj):
        perg = []
        for i in obj.pergunta_set.all():
            perg.append(i)
        return len(perg)
    
    def num_resp(self, obj):
        resp = []
        for i in obj.pergunta_set.all():
            for f in i.resposta_set.all():
                resp.append(f)
        return len(resp)

admin.site.register(Tag, TagAdmin)
    
    
class RespostaAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'votes']
    list_display = ['pergunta', 'autor', 'data', 'votes']
    list_filter = ['autor', 'data']
    search_fields = ['pergunta__titulo', 'resposta', 'autor__username', 'autor__email']
    
    class Meta:
        model = Resposta

admin.site.register(Resposta, RespostaAdmin)
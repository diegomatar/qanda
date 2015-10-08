#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz

from collections import Counter
from datetime import datetime, timedelta
from itertools import chain

from .models import Pergunta, Resposta, Tag, Comment

# Return a list of recent questions, answers and comments
def atividades_recentes(request):
    perguntas = Pergunta.objects.order_by('-timestamp')[:30]
    respostas = Resposta.objects.order_by('-timestamp')[:30]
    comentarios = Comment.objects.order_by('-timestamp')[:30]
    
    atividades = list(chain(perguntas, respostas, comentarios))
    ativ_em_ordem = sorted(atividades, key= lambda t: t.timestamp, reverse=True)[0:6]
    
    return {'atividades_recentes': ativ_em_ordem}


# Get the most active tags during the last days
def tags(request):
    last_days = 30
    now = datetime.now(pytz.utc)
    then = now - timedelta(days=last_days)
    
    # Get all content produced in the last days
    perguntas = Pergunta.objects.filter(timestamp__gte=then)
    respostas = Resposta.objects.filter(timestamp__gte=then)
    
    # Get the tags of each recent content
    used_tags = []
    for perg in perguntas:
        for tag in perg.tags.all():
            used_tags.append(tag)
    for resp in respostas:
        for tag in resp.pergunta.tags.all():
            used_tags.append(tag)
    
    # Check how many times they apears and order by appearance
    counts = Counter(used_tags).most_common()
    tags = []
    for i in counts:
        tags.append(i[0])
 
    return {'tags_todas': tags[0:10]}



# Get the most active users during last days
def active_users(request):
    last_days = 90
    now = datetime.now(pytz.utc)
    then = now - timedelta(days=last_days)
    
    # Get all content produced in the last days
    perguntas = Pergunta.objects.filter(timestamp__gte=then)
    respostas = Resposta.objects.filter(timestamp__gte=then)
    coments = Comment.objects.filter(timestamp__gte=then)
    
    # Get the author of each recent content
    autors = []
    for perg in perguntas:
        autors.append(perg.autor)
    for resp in respostas:
        autors.append(resp.autor)
    for come in coments:
        autors.append(come.autor)
            
    
    # Check how many times they apears and order by appearance
    counts = Counter(autors).most_common()
    autores = []
    for i in counts:
        autores.append(i[0])
    
    return {'usuarios': autores[0:10]}










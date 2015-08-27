from itertools import chain

from .models import Pergunta, Resposta, Tag


def atividades_recentes(request):
    perguntas = Pergunta.objects.all()
    respostas = Resposta.objects.all()
    
    atividades = list(chain(perguntas, respostas))
    ativ_em_ordem = sorted(atividades, key= lambda t: t.timestamp, reverse=True)[0:6]
    
    return {'atividades_recentes': ativ_em_ordem}


def tags(request):
    tags = Tag.objects.all()
    em_ordem = sorted(tags, key= lambda t: t.num_perguntas(), reverse=True)[:15]
    
    return {'tags_todas': em_ordem}
    
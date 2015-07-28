from django.shortcuts import render

from .models import Pergunta, Resposta, Tag

# Create your views here.
def home(request):
    
    perguntas = Pergunta.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'perguntas': perguntas,
        'tags': tags,
    }
    return render(request, 'home.html', context)


def pergunta(request, slug):
    
    pergunta = Pergunta.objects.get(slug=slug)
    
    pergunta.views += 1
    pergunta.save()
    
    context = {
        'pergunta': pergunta,
    }
    return render(request, 'perguntas/pergunta.html', context)


def categoria(request, slug):
    
    tag = Tag.objects.get(slug=slug)
    perguntas = tag.pergunta_set.all()
    
    context = {
        'tag': tag,
        'perguntas': perguntas,
    }
    return render(request, 'perguntas/tag.html', context)
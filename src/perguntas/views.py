from django.shortcuts import render, HttpResponse

from .models import Pergunta, Resposta, Tag




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



def upvote(request):
    
    perg_id = None
    if request.method == "GET":
        perg_id = request.GET['pergunta_id']
    
    votes = 0
    if perg_id:
        perg = Pergunta.objects.get(id=int(perg_id))
        if perg:
            votes = perg.votes + 1
            perg.votes = votes
            perg.save()
            
    return HttpResponse(votes)
    
    

def downvote(request):
    
    perg_id = None
    if request.method == "GET":
        perg_id = request.GET['pergunta_id']
    
    votes = 0
    if perg_id:
        perg = Pergunta.objects.get(id=int(perg_id))
        if perg:
            votes = perg.votes - 1
            perg.votes = votes
            perg.save()
            
    return HttpResponse(votes)

    
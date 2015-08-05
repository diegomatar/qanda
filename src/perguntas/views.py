from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.shortcuts import render, HttpResponse, HttpResponseRedirect


from user_profile.models import UserProfile
from .forms import PerguntaForm, RespostaForm, TagForm
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
    profile = 0
    try:
        profile = request.user.userprofile
    except:
        pass
    
    upvoted = 0
    downvoted = 0
    if profile:
        if pergunta in profile.perg_upvotes.all():
            upvoted = 1
             
        if pergunta in profile.perg_downvotes.all():
            downvoted = 1
            
    
    pergunta.views += 1
    pergunta.save()
    
    context = {
        'pergunta': pergunta,
        'upvoted': upvoted,
        'downvoted': downvoted,
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


@login_required
def upvote(request):
    print 'upvote 1'
    # Get the data being passed by get
    perg_id = None
    if request.method == "GET":
        perg_id = request.GET['pergunta_id']
        print 'upvote 2'
    votes = 0
    # If was passed any value on get
    if perg_id:
        print 'upvote 3'
        # Get the question with the id received
        perg = Pergunta.objects.get(id=int(perg_id))
        
        # Get the user profile
        profile = request.user.userprofile
        print 'upvote 4'
        # upvotes the question
        if perg:
            print 'upvote 5'
            votes = perg.votes + 1
            perg.votes = votes
            perg.save()
            print 'upvote 6'

            # forst removes from downvotes
            if perg in profile.perg_downvotes.all():
                print 'upvote 8'
                profile.perg_downvotes.remove(perg)
                profile.save()
            else:
                # after adds question to upvotes
                print 'upvote 7'
                profile.perg_upvotes.add(perg)
                profile.save()
            
    return HttpResponse(votes)
    
    
@login_required
def downvote(request):
    print 'downvote 1'
    # Get the data being passed by get
    perg_id = None
    if request.method == "GET":
        perg_id = request.GET['pergunta_id']
        print 'downvote 2'
    
    votes = 0
    # If was passed any value on get
    if perg_id:
        print 'downvote 3'
        # Get the question with the id received
        perg = Pergunta.objects.get(id=int(perg_id))
        # Get the user profile
        profile = request.user.userprofile
        print 'downvote 4'
        # downvote the question
        if perg:
            print 'downvote 5'
            votes = perg.votes - 1
            perg.votes = votes
            perg.save()
            print 'downvote 6'
            
            # removes from upvotes
            if perg in profile.perg_upvotes.all():
                print 'downvote 8'
                profile.perg_upvotes.remove(perg)
                profile.save()
            else:
                # add question to downvotes
                print 'downvote 7'
                profile.perg_downvotes.add(perg)
                profile.save()
            
    return HttpResponse(votes)


def perguntar(request):
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.autor = request.user
            form_data.slug = slugify(form_data.titulo)
            form_data.save()
            form.save_m2m()
            return HttpResponseRedirect('/')
    else:
        form = PerguntaForm()
        
    context = {
        'form': form,
    }
    
    return render(request, 'perguntas/perguntar.html', context)



def responder(request, pk):
    pergunta = Pergunta.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.pergunta = pergunta
            form_data.autor = request.user
            form_data.save()
            url = pergunta.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        form = RespostaForm()
    
    context = {
        'form': form,
        'pergunta': pergunta,
    }
     
    return render(request, 'perguntas/responder.html', context)       
            
    

    
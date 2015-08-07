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

# Upvotes a question
@login_required
def upvote(request):
    # Get the data being passed by get
    perg_id = None
    if request.method == "GET":
        perg_id = request.GET['pergunta_id']
    votes = 0
    # If was passed any value on get
    if perg_id:
        # Get the question with the id received
        perg = Pergunta.objects.get(id=int(perg_id))
        
        # Get the user profile
        profile = request.user.userprofile
        # upvotes the question
        if perg:
            votes = perg.votes + 1
            perg.votes = votes
            perg.save()

            # forst removes from downvotes
            if perg in profile.perg_downvotes.all():
                profile.perg_downvotes.remove(perg)
                profile.save()
            else:
                # after adds question to upvotes
                profile.perg_upvotes.add(perg)
                profile.save()
            
    return HttpResponse(votes)
    
# Downvotes a question
@login_required
def downvote(request):
    # Get the data being passed by get
    perg_id = None
    if request.method == "GET":
        perg_id = request.GET['pergunta_id']
    
    votes = 0
    # If was passed any value on get
    if perg_id:
        # Get the question with the id received
        perg = Pergunta.objects.get(id=int(perg_id))
        # Get the user profile
        profile = request.user.userprofile
        # downvote the question
        if perg:
            votes = perg.votes - 1
            perg.votes = votes
            perg.save()
            
            # removes from upvotes
            if perg in profile.perg_upvotes.all():
                profile.perg_upvotes.remove(perg)
                profile.save()
            else:
                # add question to downvotes
                profile.perg_downvotes.add(perg)
                profile.save()
            
    return HttpResponse(votes)


# Upvotes an answer
@login_required
def resp_upvote(request):
    # Get the data being passed by get
    resp_id = None
    if request.method == "GET":
        resp_id = request.GET['resposta_id']
    votes = 0
    # If was passed any value on get
    if resp_id:
        # Get the answer with the id received
        resp = Resposta.objects.get(id=int(resp_id))
        
        # Get the user profile
        profile = request.user.userprofile
        # upvotes the question
        if resp:
            votes = resp.votes + 1
            resp.votes = votes
            resp.save()

            # first removes from downvotes
            if resp in profile.resp_downvotes.all():
                profile.resp_downvotes.remove(resp)
                profile.save()
            else:
                # after adds question to upvotes
                profile.resp_upvotes.add(resp)
                profile.save()
            
    return HttpResponse(votes)


# Downvotes an answer
@login_required
def resp_downvote(request):
    # Get the data being passed by get
    resp_id = None
    if request.method == "GET":
        resp_id = request.GET['resposta_id']
    
    votes = 0
    # If was passed any value on get
    if resp_id:
        # Get the question with the id received
        resp = Resposta.objects.get(id=int(resp_id))
        # Get the user profile
        profile = request.user.userprofile
        # downvote the question
        if resp:
            votes = resp.votes - 1
            resp.votes = votes
            resp.save()
            
            # first removes from upvotes
            if resp in profile.resp_upvotes.all():
                profile.resp_upvotes.remove(resp)
                profile.save()
            else:
                # add question to downvotes
                profile.resp_downvotes.add(resp)
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
            
    

    
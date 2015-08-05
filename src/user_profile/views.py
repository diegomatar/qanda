from allauth.account.signals import user_signed_up
from itertools import chain

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import render


from perguntas.models import Pergunta, Resposta, Tag
from .forms import EditProfileForm, EditUserForm
from .models import UserProfile

# Create your views here.

def user_profile(request):
    
    user_data = UserProfile.objects.get(user=request.user)
    print user_data.profile_image_url()

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user_data)
        if profile_form.is_valid and user_form.is_valid:
            user_form.save()
            profile_form.save()
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=user_data)
        
    
    context ={
        'user': user_data,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user_profile/profile.html', context)

# This view creates and populates user profile with social data
@receiver(user_signed_up)
def populate_profile(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        if sociallogin.account.provider == 'facebook':
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name = sociallogin.account.extra_data['last_name']
        user.save()
        perfil = UserProfile(user=user)
        perfil.save()
        
        
        

def public_profile(request, pk):
    
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    
    perguntas = Pergunta.objects.filter(autor=user)
    respostas = Resposta.objects.filter(autor=user)
    
    atividades = list(chain(perguntas, respostas))
    ativ_em_ordem = sorted(atividades, key= lambda t: t.timestamp, reverse=True)[0:5]
    
    context = {
        'user': user,
        'profile': profile,
        'atividades': ativ_em_ordem,
    }
    
    return render(request, 'user_profile/public_profile.html', context)
    
        
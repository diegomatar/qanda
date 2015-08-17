from allauth.account.signals import user_signed_up
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse


from perguntas.models import Pergunta, Resposta, Tag
from notifications.views import new_Follow
from .forms import EditProfileForm, EditUserForm
from .models import UserProfile

# Create your views here.

@login_required
def user_profile(request):
    
    user_data = UserProfile.objects.get(user=request.user)

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
    
    if user in request.user.userprofile.follow_users.all():
        is_followed = 1
    else:
        is_followed = 0
    
    
    context = {
        'user': user,
        'profile': profile,
        'atividades': ativ_em_ordem,
        'is_followed': is_followed,
    }
    
    return render(request, 'user_profile/public_profile.html', context)


def members(request):
    
    users = UserProfile.objects.all()
    paginator = Paginator(users, 30) # Show 30 users per page
    
    page = request.GET.get('page')
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        profiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        profiles = paginator.page(paginator.num_pages)

    context = {
        'profiles': profiles,
    }

    return render(request, 'user_profile/members.html', context)
    

@login_required
def follow_user(request):
    user_id = None
    
    if request.method == "GET":
        # Get the user to be followed and its profile
        user_id = request.GET['userprofile_id']
        follow_user = User.objects.get(id=int(user_id))
        follow_user_profile = follow_user.userprofile
        followers = 0
        
        # Get the logedin user
        profile = request.user.userprofile
        user_follows = profile.follow_users.all()
        
        # Add user to be followed to the current user list
        if follow_user and follow_user not in user_follows:
            followers = follow_user_profile.followers_num + 1
            follow_user_profile.followers_num = followers
            follow_user_profile.save()
            profile.follow_users.add(follow_user)
            profile.save()
            notif = new_Follow(follow_user, request.user)
            
    return HttpResponse(followers)
            
            
        

@login_required
def unfollow_user(request):
    user_id = None
    
    if request.method == "GET":
        # Get the user to be followed and its profile
        user_id = request.GET['userprofile_id']
        unfollow_user = User.objects.get(id=int(user_id))
        follow_user_profile =unfollow_user.userprofile
        followers = 0
        
        # Get the logedin user
        profile = request.user.userprofile
        user_follows = profile.follow_users.all()
        
        # Remove user to be followed to the current user list
        if unfollow_user and unfollow_user in user_follows:
            followers = follow_user_profile.followers_num - 1
            follow_user_profile.followers_num = followers
            follow_user_profile.save()
            profile.follow_users.remove(unfollow_user)
            profile.save()
            
    return HttpResponse(followers)
        
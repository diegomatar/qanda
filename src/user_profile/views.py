from allauth.account.signals import user_signed_up
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse
from django.template.defaultfilters import slugify


from perguntas.models import Pergunta, Resposta, Tag
from notifications.views import new_Follow
from perguntas.views import suggest_topics
from .forms import EditProfileForm, EditUserForm
from .models import UserProfile



# Allow user to edit its profile
@login_required
def user_profile(request):
    
    user_data = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user_data)
        if profile_form.is_valid and user_form.is_valid:
            user_form.save()
            profile_form.save()
            slug = str(user_data.user.first_name) +' '+ str(user_data.user.last_name)
            slug = slugify(slug)
            user_data.slug = slug
            user_data.save()
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
        perfil.facebook = sociallogin.account.extra_data['link']
        perfil.save()
        
        
        
# Show the public profile information
def public_profile(request, slug):
    
    profile = UserProfile.objects.get(slug=slug)
    user = profile.user
    
    perguntas = Pergunta.objects.filter(autor=user)
    respostas = Resposta.objects.filter(autor=user)
    
    atividades = list(chain(perguntas, respostas))
    ativ_em_ordem = sorted(atividades, key= lambda t: t.timestamp, reverse=True)[0:5]
    
    is_followed = 0
    if request.user.is_authenticated():
        if user in request.user.userprofile.follow_users.all():
            is_followed = 1
    
    
    context = {
        'user': user,
        'profile': profile,
        'atividades': ativ_em_ordem,
        'is_followed': is_followed,
    }
    
    return render(request, 'user_profile/public_profile.html', context)


# Display all users
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
    

# Start following a user
@login_required
def follow_user(request):
    user_id = None
    
    if request.method == "GET":
        # Get the user to be followed and its profile
        user_id = request.GET['userprofile_id']
        follow_user = User.objects.get(id=int(user_id))
        follow_user_profile = follow_user.userprofile
        
        # Get the logedin user
        profile = request.user.userprofile
        user_follows = profile.follow_users.all()
        
        # Add user to be followed to the current user list
        if follow_user and follow_user not in user_follows:
            profile.follow_users.add(follow_user)
            profile.save()
            followers = follow_user_profile.followers_num()
            notif = new_Follow(follow_user, request.user)
            
    return HttpResponse(followers)
            
            
        
# Unfollow a user
@login_required
def unfollow_user(request):
    user_id = None
    
    if request.method == "GET":
        # Get the user to be followed and its profile
        user_id = request.GET['userprofile_id']
        unfollow_user = User.objects.get(id=int(user_id))
        unfollow_user_profile = unfollow_user.userprofile
        
        # Get the logedin user
        profile = request.user.userprofile
        user_follows = profile.follow_users.all()
        
        # Remove user to be followed to the current user list
        if unfollow_user and unfollow_user in user_follows:
            profile.follow_users.remove(unfollow_user)
            profile.save()
            followers = unfollow_user_profile.followers_num()
            
    return HttpResponse(followers)


# Show all user folowers
def user_followers(request, slug):
    profile = UserProfile.objects.get(slug=slug)
    followers = profile.user.follows.all()
    
    is_followed = 0
    if request.user.is_authenticated():
        if profile.user in request.user.userprofile.follow_users.all():
            is_followed = 1
            
    
    context = {
        'profile': profile,
        'followers': followers,
        'is_followed': is_followed,
    }
    
    return render(request, 'user_profile/followers.html', context)


# Show all user questions
def user_questions(request, slug):
    profile = UserProfile.objects.get(slug=slug)
    questions = Pergunta.objects.filter(autor=profile.user)
    
    if profile.user in request.user.userprofile.follow_users.all():
        is_followed = 1
    else:
        is_followed = 0
        
        
    context = {
        'profile': profile,
        'questions': questions,
        'is_followed': is_followed,
    }
    
    return render(request, 'user_profile/questions.html', context)


# Show all user answers
def user_answers(request, slug):
    profile = UserProfile.objects.get(slug=slug)
    answers = Resposta.objects.filter(autor=profile.user)
    
    if profile.user in request.user.userprofile.follow_users.all():
        is_followed = 1
    else:
        is_followed = 0
        
        
    context = {
        'profile': profile,
        'answers': answers,
        'is_followed': is_followed,
    }
    
    return render(request, 'user_profile/answers.html', context)
        

# Add a topic to user known topics
def add_topic_known(request):
    # Get the data being passed by get
    topic_id = None
    if request.method == "GET":
        topic_id = request.GET['topic_id']
    # If was passed any value on get
    if topic_id:
        # Get the topic with the id received
        topic = Tag.objects.get(pk=int(topic_id))
        # Get the user profile
        profile = request.user.userprofile
        # adds the topic to knowledge
        if topic and topic not in profile.knows_about.all():
            profile.knows_about.add(topic)
            profile.save()
            
    return HttpResponse()



# Remove a topic from user known topics
def remove_topic_known(request):
    # Get the data being passed by get
    topic_id = None
    if request.method == "GET":
        topic_id = request.GET['topic_id']
    # If was passed any value on get
    if topic_id:
        # Get the topic with the id received
        topic = Tag.objects.get(pk=int(topic_id))
        # Get the user profile
        profile = request.user.userprofile
        # adds the topic to knowledge
        if topic and topic in profile.knows_about.all():
            profile.knows_about.remove(topic)
            profile.save()
            
    return HttpResponse()


# Allow user to edit its known topics
def edit_user_known_topics(request):
    # get profile, topics of knowledge and aswered questions
    profile = request.user.userprofile
    current_topics = profile.knows_about.all()
    
    sugestions = suggest_topics(profile)
    
    context = {
        'sugestions': sugestions,
        'current_topics': current_topics,
    }
    
    return render(request, 'user_profile/definir_topicos.html', context)









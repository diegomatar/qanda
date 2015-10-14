#!/usr/bin/env python
# -*- coding: utf-8 -*-

from allauth.account.signals import user_signed_up
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify


from allauth.socialaccount.models import SocialAccount
from perguntas.models import Pergunta, Resposta, Tag
from notifications.views import new_Follow
from perguntas.views import suggest_topics, atividades_recentes
from .forms import EditProfileForm, EditUserForm, EditProfilePictureForm
from .models import UserProfile



# Function that retirns user social account:
def get_social_accounts(user):
    
    facebook = None
    google = None
    twitter = None
    
    facebook_list = SocialAccount.objects.filter(user_id=user.pk, provider='facebook')
    if len(facebook_list):
        facebook = facebook_list[0]
    
    google_list = SocialAccount.objects.filter(user_id=user.pk, provider='google')
    if len(google_list):
        google = google_list[0]
    
    twitter_list = SocialAccount.objects.filter(user_id=user.pk, provider='twitter')
    if len(twitter_list):
        twitter = twitter_list[0]
        
    return facebook, google, twitter



# Allow user to edit its profile
@login_required
def edit_user_profile(request):
    
    profile = request.user.userprofile
    facebook, google, twitter = get_social_accounts(request.user)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        
        if profile_form.is_valid and user_form.is_valid:
            user_form.save()
            profile_form.save()
            slug = str(profile.user.first_name) +' '+ str(profile.user.last_name)
            slug = slugify(slug)
            profile.slug = slug
            profile.save()
            messages.success(request, 'Suas informações foram atualizadas com sucesso!!')
        
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=profile)
        picture_form = EditProfilePictureForm(instance=profile)
        # Use funtion to get user social accounts
    
    context ={
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'picture_form': picture_form,
        'facebook': facebook,
        'google': google,
        'twitter': twitter,
    }
    return render(request, 'user_profile/edit_profile.html', context)


# Handle the picture submited form
def edit_user_profile_picture(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        picture_form = EditProfilePictureForm(request.POST, request.FILES, instance=profile)
        
        if picture_form.is_valid:
            picture_form.save()
            messages.success(request, 'Sua foto foi atualizadas com sucesso!!')
            
    return HttpResponseRedirect(reverse('edit_profile', args=[] ))


# This view creates and populates user profile with social data
@receiver(user_signed_up)
def populate_profile(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        print 'social login!!!'
        if sociallogin.account.provider == 'facebook':
            if not user.first_name and sociallogin.account.extra_data['first_name']:
                user.first_name = sociallogin.account.extra_data['first_name']
            if not user.last_name and sociallogin.account.extra_data['last_name']:
                user.last_name = sociallogin.account.extra_data['last_name']
            if not user.email and sociallogin.account.extra_data['email']:
                user.last_name = sociallogin.account.extra_data['email']
            user.save()
            if user.userprofile:
                perfil = user.userprofile
            else:
                perfil = UserProfile(user=user)
            perfil.facebook = sociallogin.account.get_profile_url()
            perfil.save()
        
        if sociallogin.account.provider == 'twitter':
            print 'twitter!!!'
            if not user.first_name and sociallogin.account.extra_data['name']:
                name = sociallogin.account.extra_data['name']
                user.first_name = name.split()[0]
            if not user.last_name and sociallogin.account.extra_data['name']:
                name = sociallogin.account.extra_data['name']
                user.last_name = name.split()[1]
            if not user.email and sociallogin.account.extra_data['email']:
                user.last_name = sociallogin.account.extra_data['email']
            user.save()
            if user.userprofile:
                perfil = user.userprofile
                print "perfil: %s" % perfil
            else:
                perfil = UserProfile(user=user)
            perfil.twitter = sociallogin.account.get_profile_url()
            perfil.save()
            print "perfil twitter: %s" % perfil.twitter
            
        if sociallogin.account.provider == 'google':
            if not user.first_name and sociallogin.account.extra_data['given_name']:
                user.first_name = sociallogin.account.extra_data['given_name']
            if not user.last_name and sociallogin.account.extra_data['family_name']:
                user.last_name = sociallogin.account.extra_data['family_name']
            if not user.email and sociallogin.account.extra_data['email']:
                user.last_name = sociallogin.account.extra_data['email']
            user.save()
            if user.userprofile:
                perfil = user.userprofile
            else:
                perfil = UserProfile(user=user)
            perfil.google = sociallogin.account.get_profile_url()
            perfil.save()
        
        
        
# Show the public profile information
def public_profile(request, slug):
    
    profile = UserProfile.objects.get(slug=slug)
    user = profile.user
    
    perguntas = Pergunta.objects.filter(autor=user)
    respostas = Resposta.objects.filter(autor=user)
    
    atividades = atividades_recentes(tag=None, user=user)
    
    is_followed = 0
    if request.user.is_authenticated():
        if user in request.user.userprofile.follow_users.all():
            is_followed = 1
            
    # Use funtion to get user social accounts
    facebook, google, twitter = get_social_accounts(user)
    
    print "Google: %s" % google.get_profile_url()
    
    context = {
        'user': user,
        'profile': profile,
        'atividades': atividades,
        'is_followed': is_followed,
        'facebook': facebook,
        'google': google,
        'twitter': twitter,
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
        follow_user = User.objects.get(pk=int(user_id))
        follow_user_profile = follow_user.userprofile
        
        # Get the logedin user
        profile = request.user.userprofile
        user_follows = profile.follow_users.all()
        
        # Add user to be followed to the current user list
        if follow_user:
            print 1
        if follow_user not in user_follows:
            print 2
        
        
        if follow_user and follow_user not in user_follows:
            profile.follow_users.add(follow_user)
            profile.save()
            notif = new_Follow(follow_user, request.user)
        followers = follow_user_profile.followers_num()
            
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









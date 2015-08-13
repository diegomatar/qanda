#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import NotiAnswer, NotiVote, NotiFollow
# Create your views here.

# Creates a new notification when a question is answered
def new_Answer(to_u, from_u, question):
    notif = NotiAnswer(to_user=to_u, from_user=from_u, question=question)
    notif.save()
    return notif
    

# Creates a new notification when a question in voted
def new_Vote(from_user, to_user, vote, question=None, answer=None):
    notif = NotiVote(to_user=to_user, from_user=from_user, vote=vote, question=question, answer=answer)
    notif.save()
    return notif


# Creates a new notification when someone follows someone
def new_Follow(to_user, from_user):
    notif = NotiFollow(to_user=to_user, from_user=from_user)
    notif.save()
    return notif



@login_required
def view_notification(request):
    user = request.user
    unread_a_notif = NotiAnswer.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    unread_v_notif = NotiVote.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    unread_f_notif = NotiFollow.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    
    read_a_notif = NotiAnswer.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    read_v_notif = NotiVote.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    read_f_notif = NotiFollow.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    
    unread_num_notif = len(unread_a_notif) + len(unread_v_notif) + len(unread_f_notif)
    all_unread = list(chain(unread_a_notif, unread_v_notif, unread_f_notif))
    all_read = list(chain(read_a_notif, read_v_notif, read_f_notif))
    
    for notif in all_unread:
        notif.unread = 0
        notif.save()
    
    context = {
        'num_notif': unread_num_notif,
        'unread': all_unread,
        'read': all_read,
    }
    
    return render(request, 'notifications/view_all.html', context)
    
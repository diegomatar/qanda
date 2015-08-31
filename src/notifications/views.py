#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect


from .models import NotiAnswer, NotiVote, NotiFollow, NotiComment
# Create your views here.

# Creates a new notification when a question is answered
def new_Answer(to_u, from_u, question, answer):
    notif = NotiAnswer(to_user=to_u, from_user=from_u, question=question, answer=answer)
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


# Creates a new notification when someone comments your answer
def new_Comment(to_user, from_user, answer, comment):
    notif = NotiComment(to_user=to_user, from_user=from_user, answer=answer, comment=comment)
    notif.save()
    return notif



@login_required
def view_notification(request):
    user = request.user
    unread_a_notif = NotiAnswer.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    unread_v_notif = NotiVote.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    unread_f_notif = NotiFollow.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    unread_c_notif = NotiComment.objects.filter(to_user=user).filter(unread=1).order_by('-timestamp')
    
    read_a_notif = NotiAnswer.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    read_v_notif = NotiVote.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    read_f_notif = NotiFollow.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    read_c_notif = NotiComment.objects.filter(to_user=user).filter(unread=0).order_by('-timestamp')
    
    unread_num_notif = len(unread_a_notif) + len(unread_v_notif) + len(unread_f_notif) + len(unread_c_notif)
    read_notif = list(chain(read_a_notif, read_v_notif, read_f_notif, read_c_notif))[:10]
    notifications = list(chain(unread_a_notif, unread_v_notif, unread_f_notif, unread_c_notif, read_notif))

    # Delete notifications older than 40 days
    days_to_delete = 60
    for notif in notifications:
        created = notif.timestamp.replace(tzinfo=None)
        if (datetime.now() + timedelta(days=-days_to_delete)) > created:
            print "apagar %s, para %s" % (notif.kind, notif.from_user)


    context = {
        'num_notif': unread_num_notif,
        'notifications': notifications,
    }
    
    return render(request, 'notifications/view_all.html', context)


# Mark a single notification as read
def mark_as_read(request, kind, pk):
    
    if kind == 'answer':
        notif = NotiAnswer.objects.get(pk=pk)
        notif.unread = 0
        notif.save()
    elif kind == 'vote':
        notif = NotiVote.objects.get(pk=pk)
        notif.unread = 0
        notif.save()
    elif kind == 'follow':
        notif = NotiFollow.objects.get(pk=pk)
        notif.unread = 0
        notif.save()
    elif kind == 'comment':
        notif = NotiComment.objects.get(pk=pk)
        notif.unread = 0
        notif.save()
        
    return HttpResponseRedirect(reverse('view_notification'))
    
    
# Mark all notifications as read
def mark_all_read(request):
    user = request.user
    unread_a_notif = NotiAnswer.objects.filter(to_user=user).filter(unread=1)
    unread_v_notif = NotiVote.objects.filter(to_user=user).filter(unread=1)
    unread_f_notif = NotiFollow.objects.filter(to_user=user).filter(unread=1)
    unread_c_notif = NotiComment.objects.filter(to_user=user).filter(unread=1)
    notifications = list(chain(unread_a_notif, unread_v_notif, unread_f_notif, unread_c_notif))
    
    for notif in notifications:
        notif.unread = 0
        notif.save()
        
    return HttpResponseRedirect(reverse('view_notification'))
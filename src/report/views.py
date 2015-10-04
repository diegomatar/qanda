#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from perguntas.models import Pergunta, Resposta, Comment
from user_profile.models import UserProfile
from .models import Question_Report, Answer_Report, Comment_Report, Profile_Report


# Creates a report of a object to site staff
def report_question(request, pk, kind):
    # get the question:
    question = Pergunta.objects.get(pk=pk)
    
    # get or create the report
    report, created = Question_Report.objects.get_or_create(question=question, kind=kind)
    
    #manipulate the report
    if request.user not in report.from_users.all():
        report.from_users.add(request.user)
    report.status = 1
    report.save()
    messages.warning(request, 'Obrigado, sua queixa contra esta pergunta será analisada por nossa equipe.')
    
    return HttpResponseRedirect(reverse('pergunta', args=[question.slug] ))
    
    
# Creates a report of a object to site staff
def report_answer(request, pk, kind):
    # get the question:
    answer = Resposta.objects.get(pk=pk)
    
    # get or create the report
    report, created = Answer_Report.objects.get_or_create(answer=answer, kind=kind)
    
    #manipulate the report
    if request.user not in report.from_users.all():
        report.from_users.add(request.user)
    report.status = 1
    report.save()
    messages.warning(request, 'Obrigado, sua queixa contra esta resposta será analisada por nossa equipe.')
    
    return HttpResponseRedirect(reverse('pergunta', args=[answer.pergunta.slug] ))
        
        

# Creates a report of a object to site staff
def report_comment(request, pk, kind):
    # get the question:
    comment = Comment.objects.get(pk=pk)
    
    # get or create the report
    report, created = Comment_Report.objects.get_or_create(comment=comment, kind=kind)
    
    #manipulate the report
    if request.user not in report.from_users.all():
        report.from_users.add(request.user)
    report.status = 1
    report.save()
    messages.warning(request, 'Obrigado, sua queixa contra este comentário será analisada por nossa equipe.')
    
    return HttpResponseRedirect(reverse('pergunta', args=[comment.answer.pergunta.slug] ))
    

# Creates a report of a object to site staff
def report_profile(request, pk, kind):
    # get the question:
    profile = UserProfile.objects.get(pk=pk)
    
    # get or create the report
    report, created = Profile_Report.objects.get_or_create(profile=profile, kind=kind)
    
    #manipulate the report
    if request.user not in report.from_users.all():
        report.from_users.add(request.user)
    report.status = 1
    report.save()
    messages.warning(request, 'Obrigado, sua queixa contra este usuário será analisada por nossa equipe.')
    
    return HttpResponseRedirect(reverse('profile', args=[profile.slug] ))
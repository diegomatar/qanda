#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404


from user_profile.models import UserProfile
from notifications.views import new_Answer, new_Vote, new_Comment, new_AskAnswer
from .forms import PerguntaForm, RespostaForm, TagForm, CommentForm, EditarPerguntaForm
from .models import Pergunta, Resposta, Tag, Comment



# Home view
def home(request):
    
    perguntas1 = []
    if request.user.is_authenticated() and request.user.userprofile.interests.all():
        for interest in request.user.userprofile.interests.all():
            filtered = Pergunta.objects.filter(tags__nome=interest.nome)
            for fltr in filtered:
                if fltr not in perguntas1:
                    perguntas1.append(fltr)
        perguntas1 = sorted(perguntas1, key=lambda pergunta: pergunta.score(), reverse=True)
    
    perguntas2 = []
    if len(perguntas1) < 100:
        perguntas2 = Pergunta.objects.all()
        perguntas2 = sorted(perguntas2, key=lambda pergunta: pergunta.score(), reverse=True)
    
    perguntas = perguntas1 + perguntas2
    
    
    paginator = Paginator(perguntas, 30) # Show 30 questions per page
    tags = Tag.objects.all()
    
    # Paginator:
    page = request.GET.get('page')
    try:
        perguntas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        perguntas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        perguntas = paginator.page(paginator.num_pages)
    
    cover_list = ['a', 'b', 'c', 'd', 'e', 'f']
    cover = 'jumbotron-' + cover_list[randint(0,len(cover_list)-1)]
    
    context = {
        'perguntas': perguntas,
        'tags': tags,
        'cover': cover,
    }
    return render(request, 'home.html', context)


# view pergunta: user can see a question and all its answers and comments
def pergunta(request, slug):
    
    pergunta = Pergunta.objects.get(slug=slug)
    respostas = []
    # If the user is answering the question
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        form.helper.form_action = reverse('responder', args=[pergunta.id])
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.pergunta = pergunta
            form_data.autor = request.user
            form_data.save()
            answer = form_data
            for usr in pergunta.follow_questions.all():
                notif = new_Answer(usr.user, request.user, pergunta, answer)
            
            url = pergunta.get_absolute_url()
            
            # Add the first two topics of question to user knowledge
            question_tags = pergunta.tags.all()[0:2]
            profile = request.user.userprofile
            profile.knows_about.add(*question_tags)
            # Add question to followed questions
            profile.follow_questions.add(pergunta)
            profile.save()
            return HttpResponseRedirect(url)
    else:
        form = RespostaForm()
    
        resps = pergunta.resposta_set.all()
        respostas = perguntas = sorted(resps, key=lambda resposta: resposta.votes, reverse=True)
        
        profile = 0
        try:
            profile = request.user.userprofile
        except:
            pass            
        
        pergunta.views += 1
        pergunta.save()
        
        for resp in pergunta.resposta_set.all():
            resp.views += 1
            resp.save()
    
    # Get related questions list
    related = related_questions(pergunta, 15)
    
    # Get users who can answer the question
    ask_users = user_to_answer(pergunta, 10)

    
    context = {
        'pergunta': pergunta,
        'respostas': respostas,
        'form': form,
        'ask_users': ask_users,
        'related': related,
    }
    return render(request, 'perguntas/pergunta.html', context)


# returns a list with x suggested users to answer a question
def user_to_answer(question, x):
    topics = question.tags.all()
    ask_users = []
    for tpc in topics:
        for usr in tpc.knows_about.all():
            if usr not in ask_users:
                ask_users.append(usr)
    
    ## If it is too few user, include those with good reputation
    if len(ask_users) < x:
        users = UserProfile.objects.all()
        users = sorted(users, key= lambda t: t.reputation(), reverse=True)[0:x+10]
        for usr in users:
            if usr not in ask_users:
                ask_users.append(usr)

    ## Remove those who alredy answered
    answered = question.resposta_set.all()
    for ans in answered:
        if ans.autor.userprofile in ask_users:
            ask_users.remove(ans.autor.userprofile)
    
    return ask_users[0:x]



# returns a list with x related questions:
def related_questions(question, x):
    topics = question.tags.all()
    related = []
    for tpc in topics:
        questions = tpc.pergunta_set.all()
        for qst in questions:
            if qst not in related and qst != question:
                related.append(qst)
        
    related.sort(key=lambda x: x.votes, reverse=True)
    
    if len(related) < x:
        all_questions = Pergunta.objects.order_by('-votes')[0:x+2]
        for qst in all_questions:
            if qst not in related and qst != question:
                related.append(qst)
    
    return related[0:x]


# Sugest topics based in user profile
def suggest_topics(profile):
    sugestions = []
    if profile.knows_about.all():
        for tpc in profile.knows_about.all():
            perguntas = tpc.pergunta_set.all()
            for perg in perguntas:
                for tag in perg.tags.all():
                    if (tag not in sugestions) and (tag not in profile.knows_about.all()):
                        sugestions.append(tag)
    
    if len(sugestions) < 30:
        tags = Tag.objects.all()
        tags = sorted(tags, key= lambda t: t.num_perguntas(), reverse=True)
        for tag in tags:
            if (tag not in sugestions) and (tag not in profile.knows_about.all()):
                sugestions.append(tag)
    
    return sugestions[0:30]


# Show questions that user can answer: menu responder
@login_required
def responder_perguntas(request):
    # get profile, topics of knowledge and aswered questions
    profile = request.user.userprofile
    topics = profile.knows_about.all()
    if not topics:
        return HttpResponseRedirect(reverse('edit_user_known_topics', args=[] ))
        
    
    # Get questions that user already answered or asked
    answered = []
    for resp in profile.respostas():
        if resp.pergunta not in answered:
            answered.append(resp.pergunta)
    for perg in profile.perguntas():
        if perg not in answered:
            answered.append(perg)
    
    # Create a suggested questions list
    sugested_questions = []
    for tpc in topics:
        questions = tpc.pergunta_set.all()
        for qst in questions:
            if (qst not in sugested_questions) and (qst not in answered):
                sugested_questions.append(qst)
                
    sugested_questions.sort(key=lambda x: x.votes, reverse=True)
    
    # If suggested list is small, add unaswered questions to the list:
    if len(sugested_questions) < 50:
        perguntas = Pergunta.objects.all()
        perguntas = sorted(perguntas, key= lambda t: t.num_respostas())
        
        for qst in perguntas:
            if (qst not in sugested_questions) and (qst not in answered):
                sugested_questions.append(qst)
    
    # Paginator
    paginator = Paginator(sugested_questions, 15) # Show 25 sugested_questions per page
    
    page = request.GET.get('page')
    try:
        sugested_questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sugested_questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sugested_questions = paginator.page(paginator.num_pages)
        
    form = RespostaForm()
    
    
    context = {
        'sugestions': sugested_questions,
        'form': form,
        'current_topics': topics,
    }
    
    return render(request, 'perguntas/menu_responder.html', context)



# Updates the suggested topic list
def update_topics_sugestion(request):
    profile = request.user.userprofile
    sugestions = suggest_topics(profile)
    
    context = {
            'sugestions': sugestions,
        }    
    return render(request, 'perguntas/sugest_topics.html', context)



# Show all questions of a category
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
        votes = perg.votes
        # Get the user profile
        profile = request.user.userprofile
        # upvotes the question
        if perg and perg not in profile.perg_upvotes.all():
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
                # Send a notification to the autor of the question
                new_Vote(request.user, perg.autor, 1, perg, None)
        
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
        votes = perg.votes
        # Get the user profile
        profile = request.user.userprofile
        # downvote the question
        if perg and perg not in profile.perg_downvotes.all():
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
                # Send a notification to the autor of the question
                new_Vote(request.user, perg.autor, 0, perg, None)
        
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
        votes = resp.votes
        # Get the user profile
        profile = request.user.userprofile
        # upvotes the question
        if resp and resp not in profile.resp_upvotes.all():
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
                # Send a notification to the autor of the answer
                new_Vote(request.user, resp.autor, 1, None, resp)
                
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
        votes = resp.votes
        # Get the user profile
        profile = request.user.userprofile
        # downvote the question
        if resp and resp not in profile.resp_downvotes.all():
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
                new_Vote(request.user, resp.autor, 0, None, resp)

    return HttpResponse(votes)

# User asks a new question
@login_required
def perguntar(request):
    if request.method == 'POST':

        form = PerguntaForm(request.POST)
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.autor = request.user
            form_data.slug = slugify(form_data.titulo)
            slug = form_data.slug
            # If slug is already taken, add a random number at the end of it
            try:
                Pergunta.objects.get(slug=slug)
                form_data.slug = slug + str(randint(0,100))
            except:
                pass
            
            form_data.save()
            form.save_m2m()
            
            # Add quetion to followed ones
            profile = request.user.userprofile
            profile.follow_questions.add(form_data)
            profile.save()
            messages.success(request, 'Parabéns! Sua pergunta foi publicada com sucesso!!')
            
            return HttpResponseRedirect(reverse('pergunta', args=[form_data.slug] ))
    
    else:
        if request.GET.get('q', ''):
            form = PerguntaForm(initial={'titulo': request.GET.get('q', '')})
        else:
            form = PerguntaForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'perguntas/perguntar.html', context)

# User answer a question
@login_required
def responder(request, pk):
    pergunta = Pergunta.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        form.helper.form_action = reverse('responder', args=[pergunta.id])
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.pergunta = pergunta
            form_data.autor = request.user
            form_data.save()
            notif = new_Answer(pergunta.autor, request.user, pergunta, form_data)
            url = pergunta.get_absolute_url()
            
            # Add the first two topics of question to user knowledge
            question_tags = pergunta.tags.all()[0:2]
            profile = request.user.userprofile
            profile.knows_about.add(*question_tags)
            # Add the question to followed ones
            profile.follow_questions.add(pergunta)
            profile.save()
            return HttpResponseRedirect(url)
    else:
        form = RespostaForm()
    
    context = {
        'form': form,
        'pergunta': pergunta,
    }
     
    return render(request, 'perguntas/responder.html', context)



# Allow user to edit questions
@login_required
def edit_question(request, pk):
    question = Pergunta.objects.get(pk=pk)
    # Checks if user has permission to edit the question
    if request.user == question.autor or request.user.userprofile.user_role == 'admin':
        # If is post get the data and save the edited question
        if request.method == 'POST':
            form = EditarPerguntaForm(request.POST, request.FILES, instance=question)
            if form.is_valid():
                form.save()
                messages.success(request, 'Pergunta editada com sucesso!!')
                return HttpResponseRedirect(reverse('pergunta', args=[question.slug]))
        # Otherwise, display the form to edit question:
        else:
            form = EditarPerguntaForm(instance=question)
    else:
        raise Http404
    
    context = {
        'form': form,
        'question': question,
    }
    
    return render(request, 'perguntas/editar_pergunta.html', context)



# Allow user to edit its own answer
@login_required
def edit_answer(request, pk):
    answer = Resposta.objects.get(pk=pk)
    # Checks user permission to edit the answer
    if request.user == answer.autor or request.user.userprofile.user_role == 'admin':
        # If is post, gets the data and save the edited answer
        if request.method == 'POST':
            form = RespostaForm(request.POST, request.FILES, instance=answer)
            if form.is_valid():
                    form.save()
                    messages.success(request, 'Resposta editada com sucesso!!')
                    return HttpResponseRedirect(reverse('pergunta', args=[answer.pergunta.slug]))
        # Otherwise, just display the form to edit:
        else:
            form = RespostaForm(instance=answer)
    else:
            raise Http404
        
    context = {
        'form': form,
        'resposta': answer,
    }
    
    return render(request, 'perguntas/editar-resposta.html', context)
    
    
# Allow users to comment answers
@login_required
def add_comment(request, pk=0):
    
    resp = Resposta.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.autor = request.user
            form_data.answer = resp
            form_data.save()
            new_Comment(resp.autor, request.user, resp, form_data)
            messages.success(request, 'Comentário enviado com sucesso!!')
            return HttpResponseRedirect(reverse('pergunta', args=[resp.pergunta.slug]))
    else:
        form = CommentForm()
    
    context = {
        'form': form,
        'answer': resp,
        'edit': 0,
    }
    
    return render(request, 'perguntas/comment.html', context)    


# Allow the author of the comment to edit it
@login_required
def edit_comment(request, pk=0):
    
    comment = Comment.objects.get(pk=pk)
    answer = comment.answer
    if comment and (comment.autor == request.user or request.user.userprofile.user_role == 'admin'):
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                    form.save()
                    messages.success(request, 'Comentário editado com sucesso!')
                    return HttpResponseRedirect(reverse('pergunta', args=[comment.answer.pergunta.slug]))
        else:
            form = CommentForm(instance=comment)
    
        
    
    
    context = {
        'form': form,
        'answer': answer,
        'edit': 1,
    }
    
    return render(request, 'perguntas/comment.html', context)

    
    
# Search questions to suggest on new question page
def get_question_list(max_results=0, inputed_question=''):
    qst_list = []
    qst_list1 = []
    qst_list2 = []
    qst_list3 = []
    qst_list4 = []
    qst_list5 = []
    
    if inputed_question:
        inputed = inputed_question.split()
        word = []
        for i in inputed:
            x = i.lower()
            word.append(x)  
        perguntas = Pergunta.objects.all()
        
        # Starts only afther X words are typed
        if len(word) < 0:
            return None
        
        for perg in perguntas:
            titulo = perg.titulo.lower()
            for search in word:
                result = titulo.find(search)
                if result == -1:
                    pass
                elif perg not in qst_list1:
                    qst_list1.append(perg)
                elif perg not in qst_list2:
                    qst_list2.append(perg)
                elif perg not in qst_list3:
                    qst_list3.append(perg)
                elif perg not in qst_list4:
                    qst_list4.append(perg)
                elif perg not in qst_list5:
                    qst_list5.append(perg)
            
        dup_qst_list = qst_list5 + qst_list4 + qst_list3 + qst_list2 + qst_list1
        
        for i in dup_qst_list:
            if i not in qst_list:
                qst_list.append(i)
        
    # Cuts the list to maximum results
    if max_results > 0:
        if len(qst_list) > max_results:
            qst_list = qst_list[:max_results]
        
        # Not working yet...
        # Make the searched word bold    
        for qst in qst_list:
            for search in word:
                titulo = qst.titulo.lower()
                index1 = titulo.find(search)
                if index1 != -1:
                    index2 = index1 + len(search)
                    string0 = qst.titulo
                    string1 = string0[:index1]+'<b>'+string0[index1:index2]+'</b>'+string0[index2:]
                    qst.titulo = string1

    return qst_list
    
    

# Suggests the questions searched in previwes view
def suggest_question(request):    
    qst_list = []
    inputed_question = ''
    if request.method == 'GET':
        inputed_question = request.GET['suggestion']
    qst_list = get_question_list(5, inputed_question)

    return render(request, 'perguntas/sugest_question.html', {'qst_list': qst_list,})
    

# Add the question to following list
# User starts to receive notifications from question
@login_required
def follow_question(request):
    # Get the data being passed by get
    quest_id = None
    if request.method == "GET":
        quest_id = request.GET['pergunta_id']
    # If was passed any value on get
    if quest_id:
        # Get the answer with the id received
        quest = Pergunta.objects.get(id=int(quest_id))
        # Get the user profile
        profile = request.user.userprofile
        # follows the question
        if quest and quest not in profile.follow_questions.all():
            profile.follow_questions.add(quest)
            profile.save()
            
    return HttpResponse()


# Removes the question from the followed topics
# User stops to receive notifications from question
@login_required
def unfollow_question(request):
     # Get the data being passed by get
    quest_id = None
    if request.method == "GET":
        quest_id = request.GET['pergunta_id']
    # If was passed any value on get
    if quest_id:
        # Get the answer with the id received
        quest = Pergunta.objects.get(id=int(quest_id))
        # Get the user profile
        profile = request.user.userprofile
        # unfollows the question
        if quest and quest in profile.follow_questions.all():
            profile.follow_questions.remove(quest)
            profile.save()
            
    return HttpResponse()


# Allow user to ask the question again
@login_required
def perguntar_novamente(request, pk):
    pergunta = Pergunta.objects.get(pk=pk)
    pergunta.data = datetime.today()
    pergunta.asked_count += 1
    pergunta.save()
    profile = request.user.userprofile
    if pergunta not in profile.follow_questions.all():
        profile.follow_questions.add(pergunta)
        profile.save()

    messages.success(request, 'Pronto! Você perguntou esta pergunta novamente!!')
    
    return HttpResponseRedirect(reverse('pergunta', args=[pergunta.slug]))
    
    
    
# Send the request to ask question to the selcted user
@login_required
def ask_to_answer(request):
    # Get the data being passed by get
    quest_id = None
    if request.method == "GET":
        quest_id = request.GET['pergunta_id']
        user_id = request.GET['user_id']
    # If was passed any value on get
    if quest_id and user_id:
        to_user = UserProfile.objects.get(pk=user_id)
        question = Pergunta.objects.get(pk=quest_id)
        from_user = request.user
        notif = new_AskAnswer(to_user.user, from_user, question)
        notif.save()
        profile = request.user.userprofile
        
        if question not in profile.follow_questions.all():
            profile.follow_questions.add(question)
            profile.save()
        

    return HttpResponse()



def get_topic_list(max_results=0, inputed_topic=''):
    topic_list = []
    topic_list1 = []
    topic_list2 = []
    topic_list3 = []
    topic_list4 = []
    topic_list5 = []
    topic_list6 = []
    
    if inputed_topic:
        inputed = inputed_topic.split()
        word = []
        for i in inputed:
            x = i.lower()
            word.append(x)  
        topicos = Tag.objects.all()
        
        # Starts only afther X words are typed
        if len(word) < 0:
            return None
        
        for tpc in topicos:
            nome = tpc.nome.lower()
            for search in word:
                result = nome.find(search)
                if result == -1:
                    pass
                elif tpc not in topic_list1:
                    topic_list1.append(tpc)
                elif tpc not in topic_list2:
                    topic_list2.append(tpc)
                elif tpc not in topic_list3:
                    topic_list3.append(tpc)
                elif tpc not in topic_list4:
                    topic_list4.append(tpc)
                elif tpc not in topic_list5:
                    topic_list5.append(tpc)
            
        dup_topic_list = topic_list5 + topic_list4 + topic_list3 + topic_list2 + topic_list1
        
        for i in dup_topic_list:
            if i not in topic_list:
                topic_list.append(i)
        
    # Cuts the list to maximum results
    if max_results > 0:
        if len(topic_list) > max_results:
            topic_list = topic_list[:max_results]
        
    return topic_list



# Search topics to user add in its knows_abaout
def search_topics(request):
    topic_list = []
    inputed_topic = ''
    if request.method == 'GET':
        inputed_topic = request.GET['suggestion']
    topic_list = get_topic_list(15, inputed_topic)
    
    context = {
        'inputed_topic': inputed_topic,
        'topic_list': topic_list,
    }
    return render(request, 'perguntas/search_topic.html', context)
    


# Create a new topic and add to user knowledge
def create_topic_known(request):
    topic_name = ''
    if request.method == 'GET':
        topic_name = request.GET['topic_name']
    
    # create new topic
    topic = Tag(nome=topic_name, slug=slugify(topic_name))
    topic.save()
    
    profile = request.user.userprofile
    profile.knows_about.add(topic)
    profile.save()
    
    context = {
    'topic': topic,
    }
    return HttpResponse()
    
    
# Get the users curent known topics and return as a list
def current_known_topics(request):
    if request.method == 'GET':
        current_topics = request.user.userprofile.knows_about.all()
        
        context = {
            'current_topics': current_topics,
        }
        
        return render(request, 'perguntas/user_topics.html', context)
    
    
    
    
    
    
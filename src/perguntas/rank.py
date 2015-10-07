from datetime import datetime, timedelta

#from .models import Pergunta


'''
This algorithm atributes a score to each question,
wich is used in home to display questions to users.

Factors considered:
- when was asked (recent is better)
- votes_num (more is better)
- answers_num (less answers firs)



'''

# weits the algoritm factors
factors = {
    'time': 3,
    'votes': 1,
    'answers': 0.5,
}


#  A Variable that deffines how many questions will be considered
# in deffining the ranking intervals
questions_to_consider = 50


# Returns only the considered questions
def considered():
    from .models import Pergunta
    questions = Pergunta.objects.order_by('-timestamp')
    last_questions = questions[:questions_to_consider]
    return last_questions
    
    
#  A function that return the values of days used in the ranking intervals,
# based in the days since asked from the considered questions
def get_time_intervals():
    last_questions = considered()
    time_frames = []
    now = datetime.now()
    # get how many days since each question was asked
    for qst in last_questions:
        when_asked = qst.timestamp.replace(tzinfo=None)
        days_asked = now - when_asked
        days = days_asked.days
        time_frames.append(days)
    
    # Order the list with days since asked values
    time_frames = sorted(time_frames, reverse=False)
    
    # Create the interval values:
    questions_considered = len(last_questions)
    intervals = 5
    interval_values = []
    for i in range(1, intervals):
        value = time_frames[i*(questions_considered/intervals)]
        i += 1
        interval_values.append(value)
    #print 'time interval values = %s' % interval_values
    return interval_values
    

#  A function that return the number of votes used in the ranking intervals,
# based in the votes of the considered questions
def get_votes_intervals():
    last_questions = considered()
    vote_frames = []
    for qst in last_questions:
        votes = qst.votes
        vote_frames.append(votes)
        
    # Order the list with votes values
    vote_frames = sorted(vote_frames, reverse=True)
    
    # Create the interval values:
    questions_considered = len(last_questions)
    intervals = 5
    interval_values = []
    for i in range(1, intervals):
        value = vote_frames[i*(questions_considered/intervals)]
        i += 1
        interval_values.append(value)
    #print 'votes interval values = %s' % interval_values
    return interval_values


#  A function that return the number of ansewrs used in the ranking intervals,
# based in the number of answer of the considered questions
def get_answers_intervals():
    last_questions = considered()
    answer_frames = []
    for qst in last_questions:
        answers = qst.num_respostas()
        answer_frames.append(answers)
        
    # Order the list with answers numbers
    answer_frames = sorted(answer_frames, reverse=True)

    # Create the interval values:
    questions_considered = len(last_questions)
    intervals = 5
    interval_values = []
    for i in range(1, intervals):
        value = answer_frames[i*(questions_considered/intervals)]
        i += 1
        interval_values.append(value)
    #print 'answers interval values = %s' % interval_values
    return interval_values




# Scores a list of questions question:
def score_question(question):
    
    # Time factor
    when_asked = question.timestamp.replace(tzinfo=None)
    now = datetime.now()
    time_elapsed = now - when_asked
    interval_values = get_time_intervals()

    if time_elapsed.days <= interval_values[0]:
        t_points = 100
    elif time_elapsed.days > interval_values[0] and time_elapsed.days <= interval_values[1]:
        t_points = 80
    elif time_elapsed.days > interval_values[1] and time_elapsed.days <= interval_values[2]:
        t_points = 60
    elif time_elapsed.days > interval_values[2] and time_elapsed.days <= interval_values[3]:
        t_points = 40
    else:
        t_points = 20
    #print "t_point = %s" % t_points
    #print "days since asked = %s " % time_elapsed.days
        
    
    # Votes factor:
    votes = question.votes
    interval_values = get_votes_intervals()
    
    if votes >= interval_values[0]:
        v_points = 100
    elif votes < interval_values[0] and votes >= interval_values[1]:
        v_points = 80
    elif votes < interval_values[1] and votes >= interval_values[2]:
        v_points = 60
    elif votes < interval_values[2] and votes >= interval_values[3]:
        v_points = 40
    else:
        v_points = 20
    #print "v_point = %s" % v_points
    #print "votes = %s " % votes
    
    
    # Answers factor:
    answers = question.num_respostas()
    interval_values = get_answers_intervals()
    
    if answers >= interval_values[0]:
        a_points = 100
    elif answers < interval_values[0] and answers >= interval_values[1]:
        a_points = 80
    elif answers < interval_values[1] and answers >= interval_values[2]:
        a_points = 60
    elif answers < interval_values[2] and answers >= interval_values[3]:
        a_points = 40
    else:
        a_points = 20
    #print "a_point = %s" % a_points
    #print "answers = %s " % answers
    
    rank = factors['time']*t_points + factors['votes']*v_points + factors['answers']*a_points
    #print factors['time']*t_points
    #print factors['votes']*v_points
    #print factors['answers']*a_points
    
    #print rank
    return rank
    

'''
## Run rank test
pergs = Pergunta.objects.all()
print pergs[1].titulo
score_question(pergs[1])
print pergs[10].titulo
score_question(pergs[10])
print pergs[15].titulo
score_question(pergs[15])
print pergs[20].titulo
score_question(pergs[20])
'''
import pytz # This had to be installed separately 'pip install pytz'


from datetime import datetime, timedelta, tzinfo
from operator import itemgetter
#from .models import Pergunta


'''
This algorithm atributes a score to a list of questions,

Factors considered:
- when was asked (recent is better)
- votes_num (more is better)
- answers_num (less answers first)



'''

# weight the algoritm factors
factors = {
    'time': 0.1,
    'votes': 0.1,
    'answers': 0.1,
    'followers': 0.1,
}


#  Deffines how many questions will be considered
# in deffining the ranking intervals
questions_to_consider = 1000


# Returns only the considered questions
def considered():
    from .models import Pergunta
    questions = Pergunta.objects.order_by('-timestamp')
    last_questions = questions[:questions_to_consider]
    return last_questions
    
    
#  A function that return the values of days used in the ranking intervals,
# based in the days since asked from the considered questions
def get_time_intervals(last_questions):
    time_frames = []
    now = datetime.now(pytz.utc)
    
    # get how many days since each question was asked
    for qst in last_questions:
        days_asked = now - qst.timestamp
        days = days_asked.days
        time_frames.append(days)
    
    # Order the list with days since asked values
    time_frames = sorted(time_frames, reverse=False)
    #print 'time_frames: %s' % time_frames
    
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
def get_votes_intervals(last_questions):
    vote_frames = []
    for qst in last_questions:
        votes = qst.votes
        vote_frames.append(votes)
        
    # Order the list with votes values
    vote_frames = sorted(vote_frames, reverse=True)
    #print "vote_frames = %s" % vote_frames
    
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


#  A function that return the number of answers used in the ranking intervals,
# based in the number of answer of the considered questions
def get_answers_intervals(last_questions):
    answer_frames = []
    for qst in last_questions:
        answers = qst.num_respostas()
        answer_frames.append(answers)
        
    # Order the list with answers numbers
    answer_frames = sorted(answer_frames, reverse=True)
    #print "answer_frames = %s" % answer_frames

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



#  A function that return the number of followers used in the ranking intervals,
# based in the number of followers of the considered questions
def get_followers_intervals(last_questions):
    followers_frames = []
    for qst in last_questions:
        followers = qst.followers_num()
        followers_frames.append(followers)
        
    # Order the list with followers numbers
    followers_frames = sorted(followers_frames, reverse=True)
    #print "followers_frames = %s" % followers_frames

    # Create the interval values:
    questions_considered = len(last_questions)
    intervals = 5
    interval_values = []
    for i in range(1, intervals):
        value = followers_frames[i*(questions_considered/intervals)]
        i += 1
        interval_values.append(value)
    #print 'followers interval values = %s' % interval_values
    return interval_values




# Scores a list of questions:
def score_questions(questions):
    
    #Fet considered questions
    last_questions = considered()
    
    # Get ranking intervals
    time_interval_values = get_time_intervals(last_questions)
    votes_interval_values = get_votes_intervals(last_questions)
    answers_interval_values = get_answers_intervals(last_questions)
    followers_interval_values = get_followers_intervals(last_questions)
    
    rank_data = []
    
    for question in questions:
        
        # Time factor
        now = datetime.now().now(pytz.utc)
        time_elapsed = now - question.timestamp
        
        if time_elapsed.days <= time_interval_values[0]:
            t_points = 100
        elif time_elapsed.days > time_interval_values[0] and time_elapsed.days <= time_interval_values[1]:
            t_points = 80
        elif time_elapsed.days > time_interval_values[1] and time_elapsed.days <= time_interval_values[2]:
            t_points = 60
        elif time_elapsed.days > time_interval_values[2] and time_elapsed.days <= time_interval_values[3]:
            t_points = 40
        else:
            t_points = 20
        #print "t_point = %s" % t_points
        #print "days since asked = %s " % time_elapsed.days
            
        
        # Votes factor:
        votes = question.votes
        
        if votes >= votes_interval_values[0]:
            v_points = 100
        elif votes < votes_interval_values[0] and votes >= votes_interval_values[1]:
            v_points = 80
        elif votes < votes_interval_values[1] and votes >= votes_interval_values[2]:
            v_points = 60
        elif votes < votes_interval_values[2] and votes >= votes_interval_values[3]:
            v_points = 40
        else:
            v_points = 20
        #print "v_point = %s" % v_points
        #print "votes = %s " % votes
        
        
        # Answers factor:
        answers = question.num_respostas()
        
        if answers >= answers_interval_values[0]:
            a_points = 100
        elif answers < answers_interval_values[0] and answers >= answers_interval_values[1]:
            a_points = 80
        elif answers < answers_interval_values[1] and answers >= answers_interval_values[2]:
            a_points = 60
        elif answers < answers_interval_values[2] and answers >= answers_interval_values[3]:
            a_points = 40
        else:
            a_points = 20
        #print "a_point = %s" % a_points
        #print "answers = %s " % answers
        
        
        # Followers factor
        followers = question.followers_num()
        
        if followers >= followers_interval_values[0]:
            f_points = 100
        elif followers < followers_interval_values[0] and followers >= followers_interval_values[1]:
            f_points = 80
        elif followers < votes_ifollowers_interval_valuesnterval_values[1] and followers >= followers_interval_values[2]:
            f_points = 60
        elif followers < votes_ifollowers_interval_valuesnterval_values[2] and followers >= followers_interval_values[3]:
            f_points = 40
        else:
            f_points = 20
        #print "f_points = %s" % f_points
        #print "followers = %s " % followers
        
        
        
        rank = factors['time']*t_points + factors['votes']*v_points + factors['answers']*a_points + factors['followers']*f_points
        
        ranked = []
        ranked.append(question)
        ranked.append(rank)
        
        rank_data.append(ranked)
    
    rank_data = sorted(rank_data, key=itemgetter(1), reverse=True)
    #print 'rank data = %s ' % rank_data
    
    sorted_questions = []
    for i in rank_data:
        sorted_questions.append(i[0])
    
    return sorted_questions
    

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
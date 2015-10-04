from itertools import chain

from .models import NotiAnswer, NotiVote, NotiFollow, NotiComment, NotiAsk

def unread_notifications(request):
    if request.user.is_authenticated():
        a_unread = NotiAnswer.objects.filter(to_user=request.user).filter(unread=1)
        v_unread = NotiVote.objects.filter(to_user=request.user).filter(unread=1)
        f_unread = NotiFollow.objects.filter(to_user=request.user).filter(unread=1)
        c_unread = NotiComment.objects.filter(to_user=request.user).filter(unread=1)
        ask_unread = NotiAsk.objects.filter(to_user=request.user).filter(unread=1)
        
        unread = list(chain(a_unread, v_unread, f_unread, c_unread, ask_unread))
        num_unread = len(unread)
        
        if num_unread > 0: 
            return {'num_unread': num_unread}
        else:
            return {'num_unread':''}

    
    else:
        return {'num_unread': ''}

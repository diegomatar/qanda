from itertools import chain

from .models import NotiAnswer, NotiVote, NotiFollow, NotiComment

def unread_notifications(request):
    if request.user.is_authenticated():
        a_unread = NotiAnswer.objects.filter(to_user=request.user).filter(unread=1)
        v_unread = NotiVote.objects.filter(to_user=request.user).filter(unread=1)
        f_unread = NotiFollow.objects.filter(to_user=request.user).filter(unread=1)
        c_unread = NotiComment.objects.filter(to_user=request.user).filter(unread=1)
        
        unread = list(chain(a_unread, v_unread, f_unread, c_unread))
        num_unread = len(unread)
        
        return {'num_unread': num_unread}
    else:
        return {'num_unread': 0}

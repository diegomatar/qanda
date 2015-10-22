#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pytz # This had to be installed separately 'pip install pytz'

from django import template
from datetime import date, timedelta, datetime, tzinfo
from django.utils.safestring import mark_safe

register = template.Library()
    
# Return post date as elapsed time
@register.filter
def time_ago(value):
    time = value
    now = datetime.now(pytz.utc)
    delta = now - time
    
    if delta.days > 20:
        return "{:%d de %b}".format(time)
    elif delta.days > 1:
        return "%s dias atrás" % delta.days
    elif delta.days > 0:
        return "ontem"
    elif delta.days == 0 and (delta.seconds // 3600) > 1:
        return "há %s horas" % (delta.seconds // 3600)
    elif delta.days == 0 and (delta.seconds // 3600) > 0:
        return "há %s hora" % (delta.seconds // 3600)
    elif delta.days == 0 and (delta.seconds // 60) > 1:
        return "há %s minutos" % (delta.seconds // 60)
    else:
        return "agora"
    
    
# Check if object was upvoted by user
@register.filter
def upvoted(obj, user):
    return obj.upvoted(user)

# Check if object was downvoted by user
@register.filter
def downvoted(obj, user):
    return obj.downvoted(user)


# Check if the object is followed by user
@register.filter
def followed(obj, user):
    return obj.followed(user)




# Mark all external links as nofollow
NOFOLLOW_RE = re.compile(u'<a (?![^>]*rel=["\']nofollow[\'"])' \
                         u'(?![^>]*href=["\']\.{0,2}/[^/])',
                         re.UNICODE|re.IGNORECASE)
@register.filter
def nofollow(content):
    return mark_safe(re.sub(NOFOLLOW_RE, u'<a rel="nofollow" ', content))



# Returns user bio of inputed tags
@register.filter
def userbio(user, tags):
        bio = user.userprofile.about
     
        for tg in tags:
            try:
                bio = user.userbio_set.get(tag=tg)
                return bio
            except:
                pass

        return bio
        



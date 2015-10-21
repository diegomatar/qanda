#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pytz # This had to be installed separately 'pip install pytz'

from django import template
from datetime import date, timedelta, datetime, tzinfo
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def post_date(value):
    data = value
    delta = date.today() - data

    if delta.days == 0:
        return "hoje"
    elif delta.days == 1:
        return "ontem"
    elif delta.days > 1 and delta.days < 10 :
        return "%s dias atrás" % delta.days
    else:
        return "{:%d de %b}".format(data)
    
    
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
    
    
    
@register.filter
def upvoted(obj, user):
    return obj.upvoted(user)

@register.filter
def downvoted(obj, user):
    return obj.downvoted(user)


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


# add class="responsive" to images
NOFOLLOW_RE = re.compile(u'<a (?![^>]*rel=["\']nofollow[\'"])' \
                         u'(?![^>]*href=["\']\.{0,2}/[^/])',
                         re.UNICODE|re.IGNORECASE)
@register.filter
def nofollow(content):
    return mark_safe(re.sub(NOFOLLOW_RE, u'<a rel="nofollow" ', content))


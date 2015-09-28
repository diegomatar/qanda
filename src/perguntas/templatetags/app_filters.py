#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import template
from datetime import date, timedelta

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
def upvoted(obj, user):
    return obj.upvoted(user)

@register.filter
def downvoted(obj, user):
    return obj.downvoted(user)


@register.filter
def followed(obj, user):
    return obj.followed(user)    
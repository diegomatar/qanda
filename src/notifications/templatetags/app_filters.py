#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter
def post_date(value):
    
    data = value.date()
    delta = date.today() - data

    if delta.days == 0:
        return "hoje"
    elif delta.days == 1:
        return "ontem"
    elif delta.days > 1 and delta.days < 10 :
        return "%s dias atrás" % delta.days
    else:
        return "em {:%d de %b %Y}".format(data)

    
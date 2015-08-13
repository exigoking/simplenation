import re 

from django import template
from django.http import QueryDict
register = template.Library()

@register.filter
def replace(value, args):
    qs = QueryDict(args)
    if qs.has_key('cherche') and qs.has_key('remplacement'):
        return value.replace(qs['cherche'], qs['remplacement'])
    else:
        return value
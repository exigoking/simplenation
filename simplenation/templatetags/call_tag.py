import re 

from django import template
from django.http import QueryDict
register = template.Library()

def callMethod(obj, methodName):
	method = getattr(obj, methodName)
	 
	if obj.__dict__.has_key("__callArg"):
		ret = method(*obj.__callArg)
		del obj.__callArg
		return ret
	return method()
 
def args(obj, arg):
	if not obj.__dict__.has_key("__callArg"):
		obj.__callArg = []
	 
	obj.__callArg += [arg]
	return obj
 
register.filter("call", callMethod)
register.filter("args", args)

@register.filter(name='humanize_numbers')
def humanize_numbers(value):
	if value < 1000:
		return value
	elif value >= 1000 and value < 1000000:
	    return str(round(value/float(1000),1)) + "k"
	elif value >= 1000000 and value <1000000000:
	    return str(round(value/float(1000000),1)) + "m"
	elif value >= 1000000000 :
	    return str(round(value/float(1000000000),1)) + "b"


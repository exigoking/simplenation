from django.http import HttpResponse, HttpResponseRedirect

def hello(request):
	return HttpResponse("Hello World")

def redirect_from_simplenation(request):
	return HttpResponseRedirect("/")
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from taggit.models import Tag, TaggedItem
import json
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

def index(request):
	terms_for_learners = Term.objects.order_by('-views')[:15]
	context_dict = {'terms_for_learners': terms_for_learners}

	terms_for_explainers = Term.objects.annotate(exp_count=Count('definition')).order_by('exp_count')[:15]
	context_dict['terms_for_explainers'] = terms_for_explainers
	tags = Tag.objects.annotate(term_count = Count('taggit_taggeditem_items')).order_by('-term_count')[:15]
	if tags:
		context_dict['tags'] = tags
	else:
		context_dict['no_tags_message'] = 'No tags found, sorry'

	return render(request, 'simplenation/index.html', context_dict)



def autocomplete_search(request):
	context_dict = {}
	
	params=json.loads(request.body)

	search_item = params['search_item']

	if search_item:
		
		terms = Term.objects.filter(name__icontains=search_item)
		if terms:
			context_dict['suggestions'] = terms
		else:
			HttpResponse("I cannot find it")

	else:
		context_dict['suggestions'] = None
		
	html = render_to_string('simplenation/autocomplete_results.html', context_dict)
	return HttpResponse(html)

def autocomplete_tag_search(request):
	context_dict = {}
	
	params=json.loads(request.body)

	search_item = params['search_item']

	if search_item:
		
		tags = Tag.objects.filter(name__icontains=search_item)
		if tags:
			context_dict['tag_suggestions'] = tags
		else:
			HttpResponse("I cannot find it")

	else:
		context_dict['tag_suggestions'] = None
		
	html = render_to_string('simplenation/autocomplete_tag_results.html', context_dict)
	return HttpResponse(html)

def search(request):

	context_dict = {}
	search_active = False
	if request.method=='POST':
		search_item = request.POST['search_item']
		search_active = True

		if search_item:
			context_dict['search_item'] = search_item
			terms = Term.objects.filter(name__icontains=search_item)
			if terms:
				context_dict['search_results'] = terms
			else:
				context_dict['not_found'] = "Not found"

		else:
			return HttpResponseRedirect('/simplenation/')


	else:
		pass
	context_dict['search_active'] = search_active

	return render(request, 'simplenation/index.html', context_dict)


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report, Session
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from taggit.models import Tag, TaggedItem
import json
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from datetime import datetime

def index(request):
	tags = []
	context_dict = {}
	session_registry = request.session.get('session_registry')
	session_id = request.session.get('session_id')
	pressed_tag_names = []

	if session_id:
		current_session = Session.objects.get(id = session_id)
		tags = current_session.tags.all()
		if tags:
			pressed_tags = current_session.pressed_tags.all()
			if pressed_tags:
				tag_name_1 = pressed_tags[0].name
				terms_for_explainers = Term.objects.filter(tags__name__in = [tag_name_1])
				for pressed_tag in pressed_tags:
					pressed_tag_names.append(pressed_tag.name)
					terms_for_explainers = terms_for_explainers.filter(tags__name__in = [pressed_tag.name])
				context_dict['pressed_tags'] = pressed_tags
			else:
				terms_for_explainers = Term.objects.order_by('-views')[:40]
		else:
			tags = Tag.objects.annotate(term_count = Count('taggit_taggeditem_items')).order_by('-term_count')[:15]
			for tag in tags:
				current_session.tags.add(tag)
			current_session.save()
			terms_for_explainers = Term.objects.order_by('-views')[:40]


		if not session_registry:
			request.session['session_registry'] = str(datetime.now())
		else:
			session_registry_date = datetime.strptime(session_registry[:-7], "%Y-%m-%d %H:%M:%S")
			if (datetime.now() - session_registry_date).days > 20:
				current_session.delete()
				request.session.clear()

	else:
		session = Session()
		session.save()
		request.session['session_id'] = session.id 
		request.session['session_registry'] = str(datetime.now())
		tags = Tag.objects.annotate(term_count = Count('taggit_taggeditem_items')).order_by('-term_count')[:15]
		for tag in tags:
			session.tags.add(tag)
		session.save()
		terms_for_explainers = Term.objects.order_by('-views')[:40]


	context_dict['terms_for_explainers'] = terms_for_explainers
	context_dict['tags'] = tags
	context_dict['pressed_tag_names'] = pressed_tag_names

	return render(request, 'simplenation/index.html', context_dict)



def autocomplete_search(request):
	context_dict = {}
	
	params=json.loads(request.body)

	search_item = params['search_item']

	if search_item:
		
		terms = Term.objects.filter(name__istartswith=search_item)
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
		
		tags = Tag.objects.filter(name__istartswith=search_item)[:10]
		if tags:
			context_dict['tag_suggestions'] = tags
		else:
			return HttpResponse("not_found")

	else:
		context_dict['tag_suggestions'] = None
		
	html = render_to_string('simplenation/autocomplete_tag_results.html', context_dict)
	return HttpResponse(html)

def search(request):

	context_dict = {}
	search_active = False
	is_single_object = 0
	if request.method=='POST':
		search_item = request.POST['search_item']
		search_active = True

		if search_item:
			context_dict['search_item'] = search_item
			terms = Term.objects.filter(name__istartswith=search_item)
			if terms:
				for term in terms:
					is_single_object = is_single_object + 1
				if is_single_object>1:
					context_dict['search_results'] = terms
				else:
					return HttpResponseRedirect('/simplenation/term/'+terms[0].slug)
			else:
				context_dict['not_found'] = "Not found"

		else:
			return HttpResponseRedirect('/simplenation/')


	else:
		pass
	context_dict['search_active'] = search_active

	return render(request, 'simplenation/index.html', context_dict)


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
from endless_pagination.decorators import page_template
from django.core.paginator import Paginator

def index(request, template = "simplenation/index.html", page_template = "simplenation/index_page.html"):
	tags = []
	context_dict = {}
	session_registry = request.session.get('session_registry')
	session_id = request.session.get('session_id')
	pressed_tag_names = []
	domain = request.META['HTTP_HOST']

	if session_id:
		current_session = Session.objects.get(id = session_id)
		tags = current_session.tags.all()
		if tags:
			pressed_tags = current_session.pressed_tags.all()
			if pressed_tags:
				tag_name_1 = pressed_tags[0].name
				terms_for_explainers = Term.objects.filter(tags__name__in = [tag_name_1]).order_by('-created_at','pk')
				for pressed_tag in pressed_tags:
					pressed_tag_names.append(pressed_tag.name)
					terms_for_explainers = terms_for_explainers.filter(tags__name__in = [pressed_tag.name])
				context_dict['pressed_tags'] = pressed_tags
			else:
				terms_for_explainers = Term.objects.all().order_by('-created_at','pk')
		else:
			tags = Tag.objects.annotate(term_count = Count('taggit_taggeditem_items')).order_by('-term_count')[:15]
			for tag in tags:
				current_session.tags.add(tag)
			current_session.save()
			terms_for_explainers = Term.objects.all().order_by('-created_at','pk')


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
		terms_for_explainers = Term.objects.all().order_by('-created_at','pk')

	paginator = Paginator(terms_for_explainers, 20)
	current_page = paginator.page(1)
	terms_for_explainers = current_page

	context_dict['current_page_number'] = current_page.number
	context_dict['total_number_of_pages'] = paginator.num_pages
	context_dict['terms_for_explainers'] = terms_for_explainers
	context_dict['tags'] = tags
	context_dict['pressed_tag_names'] = pressed_tag_names
	context_dict['domain'] = domain
	context_dict['page_template'] = page_template

	if request.is_ajax():
		template = page_template

	return render(request, template, context_dict)



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
					return HttpResponseRedirect('/term/'+terms[0].slug)
			else:
				context_dict['not_found'] = "Not found"

		else:
			return HttpResponseRedirect('/simplenation/')


	else:
		pass
	context_dict['search_active'] = search_active

	return render(request, 'simplenation/index.html', context_dict)


def paginate(request):
	context_dict = {}
	params = json.loads(request.body)
	page_number = params['page_number']
	number_of_tags = params['number_of_tags']
	tag_choose_list = params['tag_choose_list']
	sort_key = params['sort_key']
	sort_direction = params['sort_direction']
	if number_of_tags == 0:
		terms = Term.objects.all().order_by('-created_at','pk')
	else:
		terms = Term.objects.filter(tags__name__in = [tag_choose_list['tag_name_0']]).order_by('-created_at','pk')
		for i in range(0,number_of_tags):
			terms = terms.filter(tags__name__in = [tag_choose_list['tag_name_'+str(i)]])

	if sort_key == "posts":
		if sort_direction == "+":
			terms = terms.annotate(exp_count=Count('definition')).order_by('-exp_count','pk')
		else:
			terms = terms.annotate(exp_count=Count('definition')).order_by('exp_count','pk')
	elif sort_key == "votes":
		if sort_direction == "+":
			terms = terms.order_by('-upvotes','pk')
		else:
			terms = terms.order_by('-downvotes','pk')
	elif sort_key == "views":
		terms = terms.order_by('-views','pk')
	elif sort_key == "date":
		terms = terms.order_by('-created_at','pk')
	else:
		pass

	paginator = Paginator(terms, 20)

	if int(page_number) > paginator.num_pages:
		context_dict['success'] = False
		context_dict['no_success_message'] = 'No more pages'
		return HttpResponse(json.dumps(context_dict), content_type="application/json")

	current_page = paginator.page(int(page_number))
	terms = current_page
	if int(page_number) > paginator.num_pages:
		context_dict['terms_for_explainers'] = None
	else:
		context_dict['terms_for_explainers'] = terms

	context_dict['current_page_number'] = current_page.number
	context_dict['total_number_of_pages'] = paginator.num_pages
	html = render_to_string('simplenation/paginated_results.html', context_dict)
	return HttpResponse(html)

def sort(request):
	context_dict = {}
	params = json.loads(request.body)
	number_of_tags = params['number_of_tags']
	tag_choose_list = params['tag_choose_list']
	sort_key = params['sort_key']
	sort_direction = params['sort_direction']
	if number_of_tags == 0:
		terms = Term.objects.all().order_by('-created_at','pk')
	else:
		terms = Term.objects.filter(tags__name__in = [tag_choose_list['tag_name_0']]).order_by('-created_at','pk')
		for i in range(0,number_of_tags):
			terms = terms.filter(tags__name__in = [tag_choose_list['tag_name_'+str(i)]])

	if sort_key == "posts":
		if sort_direction == "+":
			terms = terms.annotate(exp_count=Count('definition')).order_by('-exp_count','pk')
		else:
			terms = terms.annotate(exp_count=Count('definition')).order_by('exp_count','pk')
	elif sort_key == "votes":
		if sort_direction == "+":
			terms = terms.order_by('-upvotes','pk')
		else:
			terms = terms.order_by('-downvotes','pk')
	elif sort_key == "views":
		terms = terms.order_by('-views','pk')
	elif sort_key == "date":
		terms = terms.order_by('-created_at','pk')
	else:
		pass

	paginator = Paginator(terms, 20)
	current_page = paginator.page(1)
	terms = current_page

	context_dict['current_page_number'] = current_page.number
	context_dict['total_number_of_pages'] = paginator.num_pages
	context_dict['terms_for_explainers'] = terms
	context_dict['user'] = request.user
	html = render_to_string('simplenation/tag_filtering.html', context_dict)
	return HttpResponse(html)

def about(request):
	context_dict ={}
	return render(request, 'simplenation/about.html', context_dict)

def terms(request):
	context_dict ={}
	return render(request, 'simplenation/terms.html', context_dict)

def rules(request):
	context_dict ={}
	return render(request, 'simplenation/rules.html', context_dict)

def privacy(request):
	context_dict ={}
	return render(request, 'simplenation/privacy.html', context_dict)


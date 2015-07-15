from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report, Favourite, Notification, Picture
from simplenation.forms import UserForm, ProfileForm, DefinitionForm, TermForm, PasswordResetRequestForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from simplenation.addons import last_posted_date, profanityFilter
from taggit.models import Tag, TaggedItem
from django.db.models import Count
import json
from django.core.mail import send_mail
import hashlib, datetime, random
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template import loader
from django.views.generic import *
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from djangobook.settings import PROFANITY_CHECK_THRESHOLD
from decimal import Decimal
import json
from datetime import datetime
from imagekit.processors import ResizeToFill
from django.db.models import Count

def term(request, term_name_slug):
	context_dict = {}
	liked = False
	reported = False
	report_by_explanation_id = {}
	pictures = []

	
	try:
		term = Term.objects.get(slug=term_name_slug)
		explanations = Definition.objects.filter(term = term)
		favorees = Favourite.objects.favorees_for_user(request.user)
		pictures = Picture.objects.filter(term = term)

		views = request.session.get('views_'+term.name)
		if not views:
			views = 1
		reset_last_view_time = False

		last_view = request.session.get('last_view_'+term.name)

		if last_view:
			last_view_time = datetime.strptime(last_view[:-7], "%Y-%m-%d %H:%M:%S")

			if (datetime.now() - last_view_time).seconds > 120:
			    views = views + 1
			    reset_last_view_time = True
		else:
			reset_last_view_time = True

		if reset_last_view_time:
			request.session['last_view_'+term.name] = str(datetime.now())
			request.session['views_'+term.name] = views

		term.views = views
		term.save()


		if request.user.id:
			likes = Like.objects.filter(user=request.user)
			reports = Report.objects.filter(user = request.user)

		tags = term.tags.all()

		
		for explanation in explanations:
			explanation.last_posted = last_posted_date(explanation.post_date)
			
			if request.user.id:
				like = likes.filter(definition=explanation)
				if like:
					explanation.like_text = 'Unlike'
				else:
					pass
				report = reports.filter(definition=explanation)

				if report:
					explanation.reporter = request.user.id
				else:
					pass

		
			

			if explanation.times_reported > PROFANITY_CHECK_THRESHOLD:
				explanation.delete()

			

		context_dict['term_name'] = term.name
		context_dict['explanations'] = explanations
		context_dict['term'] = term
		context_dict['tags'] = tags
		context_dict['favourites'] = favorees
		if pictures:
				context_dict['pictures'] = pictures

		if request.user.id:
			if likes:
				context_dict['likes'] = likes



		context_dict['liked'] = liked

		if request.method == 'POST' and 'add' in request.POST:
		
			form = DefinitionForm(request.POST or None)
			pictures = request.FILES.getlist('pictures')
			if form.is_valid():
				definition = form.save(commit=False)

				suspect_word_count = profanityFilter(definition.body)

				if suspect_word_count > 0:
					definition.times_reported = suspect_word_count

				definition.term = term
				definition.author = request.user.author
				definition.save()

				
				for picture in pictures:
					Picture(definition = definition, image = picture, image_thumbnail = picture, term=term).save()

				if request.user != definition.term.author.user:
					Notification(typeof = 'explanation_notification', sender = request.user, receiver = definition.term.author.user, term = term).save()

				return HttpResponseRedirect('/simplenation/term/'+ term_name_slug)
			else:
				print form.errors	

		else:
			form = DefinitionForm()

	except Term.DoesNotExist:
		pass
	
	context_dict['form'] = form
	return render(request, 'simplenation/term.html', context_dict)


@login_required
def add_tags_to_term(request):
	tag_id = None
	tag_name = None
	signal = None

	if request.method=='GET':
		tag_name = request.GET['tag_name']
		term_id = request.GET['term_id']
		signal = request.GET['signal']
		term = Term.objects.get(id = term_id)
		

		if signal == 'add':

			term.tags.add(tag_name)
			term.save()

		elif signal == 'remove':
			
			term.tags.remove(tag_name)
			term.save()
			

		else:
			pass

		return HttpResponse('Done')

	else:
		return HttpResponse('Not a GET request!')


def search_tags(request):
	context_dict = {}

	if request.method == 'GET':

		search_tag_item = request.GET['search_tag_item']
		if search_tag_item:
			tags = Tag.objects.filter(name__icontains=search_tag_item).distinct()
		else:
			tags = None

		if tags:
			context_dict['tags'] = tags
		else:
			context_dict['no_tags_message'] = 'No tags found, sorry'
			return HttpResponse('No tags found, sorry')
	else:
		context_dict['no_tags_message'] = 'No tags found, sorry'
		return HttpResponse('No tags found, sorry')

	html = render_to_string('simplenation/search_tags.html', context_dict)
	return HttpResponse(html)


def tag_select(request):
	tag_name_1 = None
	tag_name_2 = None
	tag_name_3 = None
	tag_name_4 = None
	tag_name_5 = None
	number_of_tags = None
	context_dict = {}
	tag_choose_list = {}

	#if request.method == 'POST':
			
	params=json.loads(request.body)
	
	number_of_tags = params['number_of_tags']

	if number_of_tags == 0:
		terms_tag_filtered = Term.objects.annotate(exp_count=Count('definition')).order_by('exp_count')
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})

		return HttpResponse(html)

	elif number_of_tags == 1:
		
		tag_choose_list = params['tag_choose_list']
		tag_name_1 = tag_choose_list['tag_name_1']
	
		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).distinct()
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)

	elif number_of_tags == 2:
		
		tag_choose_list = params['tag_choose_list']

		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)

	elif number_of_tags == 3:
		
		tag_choose_list = params['tag_choose_list']
		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		tag_name_3 = tag_choose_list['tag_name_3']
		

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2]).filter(tags__name__in = [tag_name_3])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)
	elif number_of_tags == 4:
		tag_choose_list = params['tag_choose_list']
		
		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		tag_name_3 = tag_choose_list['tag_name_3']
		tag_name_4 = tag_choose_list['tag_name_4']

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2]).filter(tags__name__in = [tag_name_3]).filter(tags__name__in = [tag_name_4])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)
	elif number_of_tags == 5:
		tag_choose_list = params['tag_choose_list']

		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		tag_name_3 = tag_choose_list['tag_name_3']
		tag_name_4 = tag_choose_list['tag_name_4']
		tag_name_5 = tag_choose_list['tag_name_5']

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2]).filter(tags__name__in = [tag_name_3]).filter(tags__name__in = [tag_name_4]).filter(tags__name__in = [tag_name_5])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)
	else:
		return HttpResponse('No words matching your tag filter')


	context_dict['terms_for_explainers'] = terms_tag_filtered

	
	return render(request, 'simplenation/index.html', context_dict)
	


@login_required
def add_term(request):
	context_dict = {}
	
	if request.method == 'POST':
		term_form = TermForm(request.POST or None)
		if term_form.is_valid():
			term = term_form.save(commit=False)
			term.author = request.user.author
			term.save()
			Notification(typeof = 'term_creation', sender = request.user, receiver = request.user, term = term).save()
			
			return HttpResponseRedirect('/simplenation/term/'+term.slug)
		else:
			print term_form.errors
	else:	
		term_form = TermForm()
	
	context_dict['term_form'] = term_form
	return render(request, 'simplenation/add_term.html', context_dict)


def single_tag_view(request, tag_slug):
	context_dict = {}
	tags = []
	tag = Tag.objects.get(slug = tag_slug)

	terms_for_explainers = Term.objects.filter(tags__name__in = [tag.name]).distinct()
	number_of_terms = terms_for_explainers.count()
	tags.append(tag)

	context_dict['tag'] = tag
	context_dict['terms_for_explainers'] = terms_for_explainers
	context_dict['number_of_terms'] = number_of_terms

	return render(request, 'simplenation/single_tag.html', context_dict)





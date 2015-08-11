from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report, Favourite, Notification, Picture, Session, PressedTag
from simplenation.forms import UserForm, ProfileForm, DefinitionForm, TermForm, PasswordResetRequestForm, SetPasswordForm, PictureForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from simplenation.addons import last_posted_date, profanityFilter, deleted_user_profile
from simplenation.user_views import log_user_while_post, register_user_while_post
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
from simplenation.addons import send_email

def term(request, term_name_slug):
	context_dict = {} 
	reported = False
	report_by_explanation_id = {}
	pictures = []
	context_dict['term_exists'] = True
	
	try:
		term = Term.objects.get(slug=term_name_slug)
		explanations = Definition.objects.filter(term = term).order_by('-likes')
		pictures = Picture.objects.filter(term = term)
		top_contributors = list(Author.objects.order_by('-score')[:50])
		views = request.session.get('views_'+term.name)

		if not views:
			term.views = term.views + 1
		

		view_registry = request.session.get('last_view_'+term.name)

		if view_registry:
			view_registry_date = datetime.strptime(view_registry[:-7], "%Y-%m-%d %H:%M:%S")

			if (datetime.now() - view_registry_date).days > 20:
			    request.session.clear()
		else:
			request.session['last_view_'+term.name] = str(datetime.now())
			request.session['views_'+term.name] = term.views

		term.save()


		if request.user.id:
			reports = Report.objects.filter(user = request.user)
			favorees = Favourite.objects.favorees_for_user(request.user)
			if favorees:
				favorees_of_favorees = []
				for favoree in favorees:
					favorees_of_favorees.extend(list(Favourite.objects.favorees_for_user(favoree)))
					if top_contributors:
						if favoree.author in top_contributors:
							top_contributors.remove(favoree.author)

				if favorees and favorees_of_favorees:
					favorees_of_favorees = list(set(favorees_of_favorees) - set(favorees))

				if request.user in favorees_of_favorees:
					favorees_of_favorees.remove(request.user)

				if favorees_of_favorees:
					for favoree in favorees_of_favorees:
						if favoree.author in top_contributors:
							top_contributors.remove(favoree.author)

		tags = term.tags.all()

		
		for explanation in explanations:
			explanation.last_posted = last_posted_date(explanation.post_date)

			if explanation.author == None:
				explanation.author = deleted_user_profile()
			
			if request.user.id:
				if Like.objects.has_liked(request.user, explanation):
					like = Like.objects.get(user=request.user, definition=explanation)
					if like.upvote:
						explanation.like_text = 'upvoted'
					elif like.downvote:
						explanation.like_text = 'downvoted'
					
				else:
					explanation.like_text = None

				report = reports.filter(definition=explanation)

				if report:
					explanation.reporter = request.user.id

		
			if explanation.times_reported > PROFANITY_CHECK_THRESHOLD:
				explanation.delete()

			

		context_dict['term_name'] = term.name
		context_dict['explanations'] = explanations
		context_dict['term'] = term
		context_dict['tags'] = tags
		
		if pictures:
			for picture in pictures:
				if picture.to_delete:
					picture.to_delete = False
					picture.save()
				if picture.to_add:
					picture.delete()
			pictures = Picture.objects.filter(term = term)
			context_dict['pictures'] = pictures

		if request.user.id:
			if favorees:
				context_dict['favourites'] = favorees
				if favorees_of_favorees:
					context_dict['favourites_of_favourites'] = favorees_of_favorees
			if top_contributors:
				if request.user.author in top_contributors:
					top_contributors.remove(request.user.author)
				context_dict['top_contributors'] = top_contributors


		# Posting on term page
		# Is user submitting a new post?
		if request.method == 'POST':
		
			form = DefinitionForm(request.POST or None)
			pictures = request.FILES.getlist('pictures')
			
			# Did user submit a valid post or is he sending blanks?
			if form.is_valid():

				definition = form.save(commit=False)
				
				# How many times did the user swear? Report to admins if he did
				suspect_word_count = profanityFilter(definition.body)
				if suspect_word_count > 0:
					definition.times_reported = suspect_word_count

				definition.term = term
				# Is user logged in?
				if not request.user.is_authenticated():
					# Is it login_form or registration_form?
					if 'login' in request.POST:
						response = log_user_while_post(request)
					else:
						response = register_user_while_post(request)
					
					# Was the registraion or authentication successful?
					if response['success']:
						user = response['user']
					else:
						# Seems the are some errors with registration or authentication
						if 'error_message' in response:
							context_dict['user_error_message'] = response['error_message']
						if 'user_form' in response:
							context_dict['user_form'] = response['user_form']
						context_dict['form'] = form
						context_dict['success'] = False
						return render(request, 'simplenation/term.html', context_dict)

				# Is it newly registered/logged or old one?
				if not user:
					definition.author = request.user.author
				else:
					definition.author = user.author

				definition.save()
				
				# Should we add pictures to the post if there are any?
				for picture in pictures:
					Picture(definition = definition, image = picture, image_thumbnail = picture, term=term).save()

				# Why not notify an article author that someone has expressed his thoughts about it?
				if definition.term.author:
					if request.user != definition.term.author.user:
						Notification(typeof = 'explanation_notification', sender = request.user, receiver = definition.term.author.user, term = term).save()

				return HttpResponseRedirect('/term/'+ term_name_slug)
			else:
				context_dict['post_error_message'] = 'Are you sending a blank post? If not, please try again.'

		else:
			form = DefinitionForm()

		context_dict['success'] = True
		context_dict['form'] = form


	except Term.DoesNotExist:
		context_dict['success'] = False
		context_dict['term_exists'] = False
		context_dict['no_success_message'] = "Term does not exist"
	
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

			term.tags.add(tag_name.lower())
			term.save()

		elif signal == 'remove':
			
			term.tags.remove(tag_name)
			term.save()
			

		else:
			pass

		return HttpResponse('Done')

	else:
		return HttpResponse('Invalid Form.')


def search_tags(request):
	context_dict = {}

	if request.method == 'GET':

		search_tag_item = request.GET['search_tag_item']

		session_id = request.session.get('session_id')

		if search_tag_item:
			tags = Tag.objects.filter(name__istartswith=search_tag_item).distinct()
		else:
			tags = None

		if tags:
			context_dict['tags'] = tags
			if session_id:
				session = Session.objects.get(id = session_id)
				for tag in tags:
					session.tags.add(tag)
				session.save()
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
			
	params=json.loads(request.body)
	
	number_of_tags = params['number_of_tags']
	session_id = request.session.get('session_id')

	if number_of_tags == 0:

		if session_id:
			session = Session.objects.get(id = session_id)
			pressed_tags = PressedTag.objects.filter(session = session)
			if pressed_tags:
				pressed_tags.delete()
		terms_tag_filtered = Term.objects.all().order_by('-created_at')[:40]
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})

		return HttpResponse(html)

	elif number_of_tags == 1:
		
		tag_choose_list = params['tag_choose_list']
		tag_name_1 = tag_choose_list['tag_name_1']
		
		tag_1 = Tag.objects.get(name = tag_name_1)
		if session_id:
			session = Session.objects.get(id = session_id)
			pressed_tags = PressedTag.objects.filter(session = session)
			if pressed_tags:
				pressed_tags.delete()
			session.pressed_tags.create(name=tag_1.name)
			session.save()

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).distinct()
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)

	elif number_of_tags == 2:
		
		tag_choose_list = params['tag_choose_list']

		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		
		tag_1 = Tag.objects.get(name = tag_name_1)
		tag_2 = Tag.objects.get(name = tag_name_2)
		if session_id:
			session = Session.objects.get(id = session_id)
			pressed_tags = PressedTag.objects.filter(session = session)
			if pressed_tags:
				pressed_tags.delete()
			session.pressed_tags.create(name=tag_1.name)
			session.pressed_tags.create(name=tag_2.name)
			session.save()

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)

	elif number_of_tags == 3:
		
		tag_choose_list = params['tag_choose_list']
		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		tag_name_3 = tag_choose_list['tag_name_3']
		
		tag_1 = Tag.objects.get(name = tag_name_1)
		tag_2 = Tag.objects.get(name = tag_name_2)
		tag_3 = Tag.objects.get(name = tag_name_3)
		if session_id:
			session = Session.objects.get(id = session_id)
			pressed_tags = PressedTag.objects.filter(session = session)
			if pressed_tags:
				pressed_tags.delete()
			session.pressed_tags.create(name=tag_1.name)
			session.pressed_tags.create(name=tag_2.name)
			session.pressed_tags.create(name=tag_3.name)
			session.save()

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2]).filter(tags__name__in = [tag_name_3])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)
	elif number_of_tags == 4:
		tag_choose_list = params['tag_choose_list']
		
		tag_name_1 = tag_choose_list['tag_name_1']
		tag_name_2 = tag_choose_list['tag_name_2']
		tag_name_3 = tag_choose_list['tag_name_3']
		tag_name_4 = tag_choose_list['tag_name_4']

		tag_1 = Tag.objects.get(name = tag_name_1)
		tag_2 = Tag.objects.get(name = tag_name_2)
		tag_3 = Tag.objects.get(name = tag_name_3)
		tag_4 = Tag.objects.get(name = tag_name_4)
		if session_id:
			session = Session.objects.get(id = session_id)
			pressed_tags = PressedTag.objects.filter(session = session)
			if pressed_tags:
				pressed_tags.delete()
			session.pressed_tags.create(name=tag_1.name)
			session.pressed_tags.create(name=tag_2.name)
			session.pressed_tags.create(name=tag_3.name)
			session.pressed_tags.create(name=tag_4.name)
			session.save()

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

		tag_1 = Tag.objects.get(name = tag_name_1)
		tag_2 = Tag.objects.get(name = tag_name_2)
		tag_3 = Tag.objects.get(name = tag_name_3)
		tag_4 = Tag.objects.get(name = tag_name_4)
		tag_5 = Tag.objects.get(name = tag_name_5)
		if session_id:
			session = Session.objects.get(id = session_id)
			pressed_tags = PressedTag.objects.filter(session = session)
			if pressed_tags:
				pressed_tags.delete()
			session.pressed_tags.create(name=tag_1.name)
			session.pressed_tags.create(name=tag_2.name)
			session.pressed_tags.create(name=tag_3.name)
			session.pressed_tags.create(name=tag_4.name)
			session.pressed_tags.create(name=tag_5.name)
			session.save()

		terms_tag_filtered = Term.objects.filter(tags__name__in = [tag_name_1]).filter(tags__name__in = [tag_name_2]).filter(tags__name__in = [tag_name_3]).filter(tags__name__in = [tag_name_4]).filter(tags__name__in = [tag_name_5])
		html = render_to_string('simplenation/tag_filtering.html', {'terms_tag_filtered': terms_tag_filtered})
		
		return HttpResponse(html)
	else:
		return HttpResponse('No words matching your tag filter')


	context_dict['terms_for_explainers'] = terms_tag_filtered

	
	return render(request, 'simplenation/index.html', context_dict)
	


def tag_deselect(request):

	params=json.loads(request.body)
	
	tag_name = params['tag_name']
	session_id = request.session.get('session_id')
	if request.method == 'POST':
		session = Session.objects.get(id = session_id)
		tag = Tag.objects.get(name = tag_name)
		session.tags.remove(tag)
		pressed_tag = PressedTag.objects.filter(name = tag_name)
		if pressed_tag:
			pressed_tag.delete()

	else:
		return HttpResponse("Invalid Form.")

	return HttpResponse("Success")



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
			
			return HttpResponseRedirect('/term/'+term.slug)
		else:
			str1 = 'exists'
			str2 = term_form.errors.as_text()
			str2 = " ".join(str2.split())
			if 'exists' in str2:
				context_dict['errors'] = 'topic already exists.'
			elif 'required' in str2:
				context_dict['errors'] = 'it was a blank'
			else:
				context_dict['errors'] = term_form.errors
	else:	
		term_form = TermForm()
	
	context_dict['term_form'] = term_form
	return render(request, 'simplenation/add_term.html', context_dict)


def single_tag_view(request, tag_slug):
	context_dict = {}
	tags = []
	tag = Tag.objects.get(slug = tag_slug)
	session_id = request.session.get('session_id')
	if session_id:
		session = Session.objects.get(id = session_id)
		session.tags.add(tag)
		session.save()

	terms_for_explainers = Term.objects.filter(tags__name__in = [tag.name]).distinct()
	number_of_terms = terms_for_explainers.count()
	tags.append(tag)

	context_dict['tag'] = tag
	context_dict['terms_for_explainers'] = terms_for_explainers
	context_dict['number_of_terms'] = number_of_terms

	return render(request, 'simplenation/single_tag.html', context_dict)





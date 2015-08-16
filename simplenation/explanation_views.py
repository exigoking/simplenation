from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report, Notification, Picture
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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.views.generic import *
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from djangobook.settings import PROFANITY_CHECK_THRESHOLD
from decimal import Decimal
import json
 


@login_required 
def edit_exp(request):

	if request.method == 'POST':
		explanation_id = request.POST.get('explanation_id', False)
		
		explanation = Definition.objects.get(id = explanation_id)
		pictures = Picture.objects.filter(definition = explanation)
		signal = request.POST['signal']

		if signal == 'edit':

			if pictures:
				for picture in pictures:
					if picture.to_delete:
						picture.delete()
					elif picture.to_add:
						picture.to_add=False
						picture.save()

			explanation.body = request.POST['body']
			suspect_word_count = profanityFilter(explanation.body)
			if suspect_word_count > 0:
				explanation.times_reported = suspect_word_count

			explanation.save()
			html = render_to_string('simplenation/edit_comment.html', {'user':request.user, 'explanation':explanation})
			return HttpResponse(html)

		elif signal == 'delete':

			if pictures:
				pictures.delete()
			explanation.delete()
			return HttpResponse('Success-deleted')
		else:
			pass

		return HttpResponse('Neither edited or deleted')	
	else:
		pass

	
	return HttpResponse('Request was not Post.')


@login_required
def add_like(request):

	explanation_id = None

	if request.method == 'POST':
		params=json.loads(request.body)
		explanation_id = params['explanation_id']
		signal = params['signal']


	if explanation_id:

		explanation = Definition.objects.get(id = explanation_id)

		if not Like.objects.has_liked(request.user, explanation):
			like = Like()
			like.user = request.user
			like.definition = explanation

			if signal == 'up':
				like.upvote = True
				like.downvote = False
				explanation.likes = explanation.likes + 1
				explanation.author.score = explanation.author.score + Decimal('0.03')
				explanation.author.num_of_likes = explanation.author.num_of_likes + 1
			elif signal == 'down':
				like.downvote = True
				like.upvote = False
				explanation.likes = explanation.likes - 1
				if explanation.likes < 0:
					explanation.likes = 0
				explanation.author.score = explanation.author.score - Decimal('0.03')
				if explanation.author.score < 0:
					explanation.author.score = 0
				explanation.author.num_of_likes = explanation.author.num_of_likes - 1

			like.save()
			explanation.save()
			explanation.author.save()
			likes = explanation.likes
 	
		else:
			like = Like.objects.get(user = request.user, definition=explanation)
			if like.upvote:
				if signal == 'down':
					like.downvote = True
					like.upvote = False
					explanation.likes = explanation.likes - 2
					if explanation.likes < 0:
						explanation.likes = 0
					explanation.author.score = explanation.author.score - Decimal('0.06')
					if explanation.author.score < 0:
						explanation.author.score = 0
					explanation.author.num_of_likes = explanation.author.num_of_likes - 2

			elif like.downvote:
				if signal == 'up':
					like.upvote = True
					like.downvote = False
					if explanation.likes == 0:
						explanation.likes = explanation.likes + 1
					else:
						explanation.likes = explanation.likes + 2
					explanation.author.score = explanation.author.score + Decimal('0.06')
					explanation.author.num_of_likes = explanation.author.num_of_likes + 2

			like.save()
			explanation.save()
			explanation.author.save()
			likes = explanation.likes
			
	else:
		return HttpResponse("Invalid form.")

	return HttpResponse(likes)


@login_required
def remove_like(request):

	explanation_id = None

	if request.method == 'POST':
		params=json.loads(request.body)
		explanation_id = params['explanation_id']
		signal = params['signal']

	if explanation_id:
		explanation = Definition.objects.get(id = explanation_id)
		like = Like.objects.get(user = request.user, definition = explanation)
		if like:
			like.delete()
			if signal == "up":
				explanation.likes = explanation.likes - 1
				if explanation.likes < 0:
					explanation.likes = 0
				explanation.author.score = explanation.author.score - Decimal('0.03')
				explanation.author.num_of_likes = explanation.author.num_of_likes - 1
				if explanation.author.score < 0:
					explanation.author.score = 0
			elif signal == "down":
				if explanation.likes == 0:
					explanation.likes = 0
				else:
					explanation.likes = explanation.likes + 1
				explanation.author.score = explanation.author.score + Decimal('0.03')
				explanation.author.num_of_likes = explanation.author.num_of_likes + 1
				
			explanation.save()
			explanation.author.save()
			likes = explanation.likes

		else:
			return HttpResponse("Already removed like.")

	else:
		return HttpResponse("Invalid Form.")

	return HttpResponse(likes)




@login_required
def report_explanation(request):

	reported = False
	explanation_id = None
	explanation = None
	if request.method == 'GET':
		explanation_id = request.GET['explanation_id']
		
	
	reports = 0
	if explanation_id:
		explanation = Definition.objects.get(id = explanation_id)
		reports = Report.objects.filter(definition = explanation)
		if reports:
			for report in reports:
					if report.user.username == request.user.username:
						report.delete()
						explanation.report = explanation.report - 1
						explanation.save()
						
					else:
						report.user = request.user
						explanation.times_reported = explanation.times_reported + 1
						report.save()
						explanation.save()
						reported = True
						
		else:
			report = Report()
			report.user = request.user
			report.definition = explanation
			report.save()
			explanation.times_reported = explanation.times_reported + 1
			explanation.save()
			reported = True
			
		reports = explanation.times_reported
	else:
		pass

	html = render_to_string('simplenation/reporting.html', {'reported':reported,'explanation':explanation})

	return HttpResponse(html)
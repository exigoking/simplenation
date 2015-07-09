from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report
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
 



def index(request):
	terms_for_learners = Term.objects.order_by('-views')[:15]
	context_dict = {'terms_for_learners': terms_for_learners}

	terms_for_explainers = Term.objects.annotate(exp_count=Count('definition')).order_by('exp_count')
	context_dict['terms_for_explainers'] = terms_for_explainers
	tags = Tag.objects.annotate(term_count = Count('taggit_taggeditem_items')).order_by('-term_count')[:20]
	if tags:
		context_dict['tags'] = tags
	else:
		context_dict['no_tags_message'] = 'No tags found, sorry'

	return render(request, 'simplenation/index.html', context_dict)

#@login_required
def profile(request, profile_name_slug):
	context_dict = {}

	try:
		author = Author.objects.get(slug=profile_name_slug)
		explanations = Definition.objects.filter(author = author).order_by('-likes')

		context_dict['explanations'] = explanations
		context_dict['author'] = author
		context_dict['profile_name'] = author.user.username
		context_dict['profile_email'] = author.user.email
		context_dict['profile_bio'] = author.bio
		if author.picture: 
			context_dict['profile_picture'] = author.picture
		else:
			pass

	except Author.DoesNotExist:
		pass

	return render(request, 'simplenation/profile.html', context_dict)

@login_required
def edit_profile(request, profile_name_slug):
	context_dict = {}
	context_dict['edited'] = False
	author = Author.objects.get(slug = profile_name_slug)
	context_dict['author'] = author
	context_dict['profile_name'] = author.user.username
	context_dict['profile_email'] = author.user.email
	context_dict['profile_bio'] = author.bio

	if request.method == 'POST':
		if request.POST['username']:
			username = request.POST['username']
			user = User.objects.get(username = username)
			if user:
				if user is request.user:
					context_dict['existing_username_error']="The username already exists."
					return render(request, 'simplenation/edit_profile.html', context_dict)
				else:
					pass
			else:
				author.user.username = username
		else:
			pass
		if request.POST['email']:
			author.user.email = request.POST['email']
		else:
			pass
		if request.POST['bio']:
			author.bio = request.POST['bio']
		else:
			pass

		if 'picture' in request.FILES:
				author.picture = request.FILES['picture']
		else:
			pass
		
		author.save()
		context_dict['edited'] = True
		return HttpResponseRedirect('/simplenation/profile/'+author.slug)

	else:
		pass

	return render(request, 'simplenation/edit_profile.html', context_dict)

def term(request, term_name_slug):
	context_dict = {}
	liked = False
	reported = False
	report_by_explanation_id = {}
	
	
	try:
		term = Term.objects.get(slug=term_name_slug)
		explanations = Definition.objects.filter(term = term)

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
		

		if request.user.id:
			if likes:
				context_dict['likes'] = likes


		context_dict['liked'] = liked

		if request.method == 'POST' and 'add' in request.POST:
		
			form = DefinitionForm(request.POST or None)
			if form.is_valid():
				definition = form.save(commit=False)

				suspect_word_count = profanityFilter(definition.body)

				if suspect_word_count > 0:
					definition.times_reported = suspect_word_count

				definition.term = term
				definition.author = request.user.author
				definition.save()
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
def edit_exp(request):

	if request.method == 'POST':
		explanation_id = request.POST.get('explanation_id', False)
		
		explanation = Definition.objects.get(id = explanation_id)
		signal = request.POST['signal']

		if signal == 'edit':

			explanation.body = request.POST['body']
			suspect_word_count = profanityFilter(explanation.body)
			if suspect_word_count > 0:
				explanation.times_reported = suspect_word_count

			explanation.save()
			html = render_to_string('simplenation/edit_comment.html', {'user':request.user, 'explanation':explanation})
			return HttpResponse(html)

		elif signal == 'delete':
			explanation.delete()
			return HttpResponse('Success-deleted')
		else:
			pass

		return HttpResponseRedirect('Neither edited or deleted')	
	else:
		pass

	
	return HttpResponse('Request was not Post.')

@login_required
def like_explanation(request):

	
	explanation_id = None
	if request.method == 'GET':
		explanation_id = request.GET['explanation_id']
		
	
	likes = 0
	if explanation_id:
		explanation = Definition.objects.get(id = explanation_id)
		author = explanation.author
		likes = Like.objects.filter(definition = explanation)
		if likes:
			for like in likes:
					if like.user.username == request.user.username:
						like.delete()
						explanation.likes = explanation.likes - 1
						explanation.save()
						author.score = author.score - Decimal('0.01')
						author.num_of_likes = author.num_of_likes - 1
						author.save()
						
						
					else:
						like.user = request.user
						explanation.likes = explanation.likes + 1
						like.save()
						explanation.save()
						author.score = author.score + Decimal('0.01')
						author.num_of_likes = author.num_of_likes + 1
						author.save()
						
		else:
			like = Like()
			like.user = request.user
			like.definition = explanation
			like.save()
			explanation.likes = explanation.likes + 1
			explanation.save()
			author.score = author.score + Decimal('0.01')
			author.num_of_likes = author.num_of_likes + 1
			author.save()

		likes = explanation.likes
	else:
		pass

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
	#else:
	#	pass

	
	return render(request, 'simplenation/index.html', context_dict)


def register(request):
	
	context_dict = {}
	context_dict['registered'] = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = ProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			username = user_form.cleaned_data['username']
			email = user_form.cleaned_data['email']


			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
			account_deletion_key = hashlib.sha1(salt+email).hexdigest()   
			
			#user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.account_deletion_key = account_deletion_key

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			context_dict['registered'] = True


			email_subject = 'From Simplenation, with love'
			email_body = "Dear %s, thanks for signing up. Welcome! \n\n We do NOT do email confirmation \n\n But you can DELETE your account HERE: http://dev.djangobook.com/simplenation/account_deletion/%s" % (username, account_deletion_key)
			send_mail(email_subject, email_body, 'headquarters@simplenation.com',[email], fail_silently=False)

			new_user = authenticate(username = request.POST['username'], password = request.POST['password1'])
			login(request, new_user)

			if request.POST["next"] is not "":
				return HttpResponseRedirect(request.POST["next"])
			else:
				return HttpResponseRedirect('/simplenation/')
			#return HttpResponseRedirect('/simplenation/')
		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = ProfileForm()

	context_dict['next'] = request.GET.get('next', '')
	context_dict['user_form'] = user_form
	context_dict['profile_form'] = profile_form

	return render(request, 'simplenation/registration_form.html', context_dict)


def account_deletion(request, account_deletion_key):
    context_dict = {}
    profile = get_object_or_404(Author, account_deletion_key=account_deletion_key)
    if request.method == 'POST':
    	if 'yes' in request.POST:
    		user = profile.user
    		profile.delete()
    		user.delete()
    		return HttpResponseRedirect('/simplenation/')
    	else:
    		return HttpResponseRedirect('/simplenation/')

    else:
    	user = profile.user
    	if user.is_authenticated:
    		context_dict['username'] = user.username
    	else:
    		context_dict['username'] = user.username

    	context_dict['account_deletion_key'] = account_deletion_key

    return render(request, 'simplenation/account_deletion.html', context_dict)


def user_login(request):
	context_dict = {}
	if request.method == 'POST':
		
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request,user)
				if request.POST["next"] is not "":
					return HttpResponseRedirect(request.POST["next"])
				else:
					return HttpResponseRedirect('/simplenation/')

			else:
				messages.error(request, 'Your account has been disabled')
				context_dict['login_error_message'] = 'Your account has been disabled'
		else:
			messages.error(request, 'Invalid username or password')
			context_dict['login_error_message'] = 'Invalid username or password'

	context_dict['next'] = request.GET.get('next', '')
		
	return render(request, 'simplenation/signin.html', context_dict) 	

@login_required
def user_logout(request):
	
	logout(request)
	
	return HttpResponseRedirect('/simplenation/')

@login_required
def add_term(request):
	context_dict = {}
	
	if request.method == 'POST':
		term_form = TermForm(request.POST or None)
		if term_form.is_valid():
			term = term_form.save(commit=False)
			term.save()
			return HttpResponseRedirect('/simplenation/term/'+term.slug)
		else:
			print term_form.errors
	else:	
		term_form = TermForm()
	
	context_dict['term_form'] = term_form
	return render(request, 'simplenation/add_term.html', context_dict)

def password_sent_confirmation(request):
	context_dict = {}

	return render(request,'simplenation/password_sent_confirmation.html')


class PasswordResetRequestView(FormView):
	template_name = "simplenation/password_reset_page.html"
	success_url = "/simplenation/password_sent_confirmation/"
	form_class = PasswordResetRequestForm

	@staticmethod
	def validate_email_address(email):
		try:
			validate_email(email)
			return True
		except ValidationError:
			return False

	def post(self, request, *args, **kwargs):
		data = None
		form = self.form_class(request.POST)

		if form.is_valid():
			data = form.cleaned_data['email_or_username']

		if self.validate_email_address(data) is True:
			associated_users= User.objects.filter(email= data)
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': request.META['HTTP_HOST'],
						'site_name': 'dev.djangobook.com',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					subject_template_name='registration/password_reset_subject.txt'
					email_template_name='registration/password_reset_email.html'
					subject = loader.render_to_string(subject_template_name, c)
					subject = ''.join(subject.splitlines())
					email = loader.render_to_string(email_template_name, c)
					send_mail(subject, email, 'headquarters@simplenation.com' , [user.email], fail_silently=False)

				result = self.form_valid(form)
				messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
				return result

			result = self.form_invalid(form)
			messages.error(request, 'No user is associated with this email address')
			return result

		else:
			associated_users= User.objects.filter(username=data)
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': request.META['HTTP_HOST'],
						'site_name': 'dev.djangobook.com',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					subject_template_name='registration/password_reset_subject.txt'
					email_template_name='registration/password_reset_email.html'
					subject = loader.render_to_string(subject_template_name, c)
					subject = ''.join(subject.splitlines())
					email = loader.render_to_string(email_template_name, c)
					send_mail(subject, email, 'headquarters@simplenation.com' , [user.email], fail_silently=False)

				result = self.form_valid(form)
				messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
				return result

			result = self.form_invalid(form)
			messages.error(request, 'No user is associated with this username')
			return result

		messages.error(request, 'Invalid Input')
		return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
	template_name = "simplenation/password_reset_page.html"
	success_url = '/simplenation/signin/'
	form_class = SetPasswordForm

	def post(self, request, uidb64=None, token=None, *arg, **kwargs):
		UserModel = get_user_model()
		form = self.form_class(request.POST)
		assert uidb64 is not None and token is not None
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = UserModel._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
			user = None

		if user is not None and default_token_generator.check_token(user, token):
			if form.is_valid():
				new_password= form.cleaned_data['new_password2']
				user.set_password(new_password)
				user.save()
				messages.success(request, 'Password has been reset.')
				return self.form_valid(form)
			else:
				messages.error(request, 'Password reset has not been unsuccessful.')
				return self.form_invalid(form)
		else:
			messages.error(request,'The reset password link is no longer valid.')
			return self.form_invalid(form)





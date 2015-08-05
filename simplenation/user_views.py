from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report, Favourite
from simplenation.forms import UserForm, ProfileForm, DefinitionForm, TermForm, PasswordResetRequestForm, SetPasswordForm
from simplenation.addons import simplenation_email_validation, simplenation_username_validation, awesomeUsernames, last_posted_date, send_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json, random
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
from djangobook.settings import EMAIL_HOST_USER, SITE_NAME, SITE_IP



def profile(request, profile_name_slug):
	context_dict = {}

	try:
		author = Author.objects.get(slug=profile_name_slug)
		explanations = Definition.objects.filter(author = author).order_by('-post_date')

		favorees = Favourite.objects.favorees_for_user(author.user)
		favoree_count = Favourite.objects.favoree_count(author.user)

		if request.user.is_authenticated():
			if not Favourite.objects.is_favoree(request.user, author.user):
				context_dict['favorite_button_class'] = None
				context_dict['favor_button_text'] = "Add to favorites"
			else:
				context_dict['favorite_button_class'] = "is-favorite"
				context_dict['favor_button_text'] = "Added to favourites"
	
		if explanations:
			for explanation in explanations:
				explanation.last_posted = last_posted_date(explanation.post_date)

		context_dict['explanations'] = explanations
		context_dict['author'] = author
		context_dict['profile_name'] = author.user.username
		context_dict['profile_email'] = author.user.email
		context_dict['profile_bio'] = author.bio
		context_dict['favourites'] = favorees
		context_dict['favourites_count'] = favoree_count

		if author.picture: 
			context_dict['profile_picture'] = author.picture
		context_dict['success'] = True

	except Author.DoesNotExist:
		context_dict['success'] = False
		context_dict['no_success_message'] = 'User does not exist.'

	return render(request, 'simplenation/profile.html', context_dict)



@login_required
def edit_profile(request, profile_name_slug):
	context_dict = {}
	context_dict['edited'] = False
	author = Author.objects.get(slug = profile_name_slug)
	context_dict['author'] = author
	context_dict['profile_name'] = author.user.username
	context_dict['profile_email'] = author.user.email

	if request.method == 'POST':		

		if request.POST['username']:
			username_for_validation = request.POST['username']
			if not simplenation_username_validation(username_for_validation):
				context_dict['profile_edit_error_message'] = "Username is a bit invalid, try something awesome like "+"'"+random.choice(awesomeUsernames)+"'"
				context_dict['next'] = request.GET.get('next', '')
				return render(request, 'simplenation/edit_profile.html', context_dict)

			username = request.POST['username']
			users = User.objects.filter(username = username)
			if users:
				for user in users:
					if user.id != request.user.id:
						context_dict['profile_edit_error_message']="Username already exists."
						return render(request, 'simplenation/edit_profile.html', context_dict)
				
			
			author.user.username = username
		
		if request.POST['email']:
			email_for_validation = request.POST['email']
			if not simplenation_email_validation(email_for_validation):
				context_dict['profile_edit_error_message'] = "Please enter correct email."
				context_dict['next'] = request.GET.get('next', '')
				return render(request, 'simplenation/edit_profile.html', context_dict)

			email = request.POST['email']
			users = User.objects.filter(email = email)
			if users:
				for user in users:
					if user.id != request.user.id:
						context_dict['profile_edit_error_message']="Email already exists."
						return render(request, 'simplenation/edit_profile.html', context_dict)

			author.user.email = request.POST['email']
		

		if 'picture' in request.FILES:
				author.picture = request.FILES['picture']
		
		author.user.save()
		author.save()
		context_dict['edited'] = True
		return HttpResponseRedirect('/simplenation/profile/'+author.slug)

	else:
		context_dict['profile_edit_error_message']= None

	return render(request, 'simplenation/edit_profile.html', context_dict)




def register(request):
	
	context_dict = {}
	context_dict['registered'] = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = ProfileForm(data=request.POST)

		if not 'username' in request.POST:
			context_dict['registration_error_message'] = "Please enter username."
			context_dict['next'] = request.GET.get('next', '')
			context_dict['user_form'] = user_form
			context_dict['profile_form'] = profile_form
			return render(request, 'simplenation/registration_form.html', context_dict)

		if not 'email' in request.POST:
			context_dict['registration_error_message'] = "Please enter email."
			context_dict['next'] = request.GET.get('next', '')
			context_dict['user_form'] = user_form
			context_dict['profile_form'] = profile_form
			return render(request, 'simplenation/registration_form.html', context_dict)

		if not 'password1' in request.POST:
			context_dict['registration_error_message'] = "Please enter password."
			context_dict['next'] = request.GET.get('next', '')
			context_dict['user_form'] = user_form
			context_dict['profile_form'] = profile_form
			return render(request, 'simplenation/registration_form.html', context_dict)

		email_for_validation = request.POST['email']
		if not simplenation_email_validation(email_for_validation):
			context_dict['registration_error_message'] = "Please enter correct email."
			context_dict['next'] = request.GET.get('next', '')
			context_dict['user_form'] = user_form
			context_dict['profile_form'] = profile_form
			return render(request, 'simplenation/registration_form.html', context_dict)

		username_for_validation = request.POST['username']
		if not simplenation_username_validation(username_for_validation):
			context_dict['registration_error_message'] = "Username is a bit invalid, try something awesome like "+"'"+random.choice(awesomeUsernames)+"'"
			context_dict['next'] = request.GET.get('next', '')
			context_dict['user_form'] = user_form
			context_dict['profile_form'] = profile_form
			return render(request, 'simplenation/registration_form.html', context_dict)

		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			username = user_form.cleaned_data['username']
			email = user_form.cleaned_data['email']


			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
			account_deletion_key = hashlib.sha1(salt+email).hexdigest()   
			
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.account_deletion_key = account_deletion_key

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			context_dict['registered'] = True

			email_data = {
				'email': email,
				'domain': request.META['HTTP_HOST'],
				'site_name': SITE_NAME,
				'account_deletion_key': account_deletion_key,
				'receiver_username': username,
				'site_email': EMAIL_HOST_USER,
				'protocol': 'http',
			}
			subject_template_name='simplenation/registration_notification_subject.txt'
			email_template_name='simplenation/registration_notification_email.html'
			
			if not send_email(email_data, subject_template_name, email_template_name):
				context_dict['registration_error_message'] = "Couldn't send confirmation email."
				context_dict['next'] = request.GET.get('next', '')
				context_dict['user_form'] = user_form
				context_dict['profile_form'] = profile_form
				return render(request, 'simplenation/registration_form.html', context_dict)

			new_user = authenticate(username = request.POST['username'], password = request.POST['password1'])
			login(request, new_user)

			if request.POST["next"] is not "":
				return HttpResponseRedirect(request.POST["next"])
			else:
				return HttpResponseRedirect('/simplenation/')
			
		else:
			context_dict['user_form_errors'] = user_form.errors
			context_dict['profile_form_errors'] = profile_form.errors

	else:
		user_form = UserForm()
		profile_form = ProfileForm()

	context_dict['next'] = request.GET.get('next', '')
	context_dict['user_form'] = user_form
	context_dict['profile_form'] = profile_form

	return render(request, 'simplenation/registration_form.html', context_dict)


@login_required
def email_confirmation(request, account_deletion_key):
    author = get_object_or_404(Author, account_deletion_key=account_deletion_key)
    author.active = True
    author.save()
    return HttpResponseRedirect('/simplenation/')



def user_login(request):
	context_dict = {}

	if request.user.is_active:
		if request.GET.get('next', ''):
			next = request.GET.get('next', '')
		else:
			next = '/simplenation/'
		return HttpResponseRedirect(next)


	if request.method == 'POST':
		
		if not 'email_or_username' in request.POST:
			context_dict['login_error_message'] = 'Please enter username or email.'
			context_dict['next'] = request.GET.get('next', '')
			return render(request, 'simplenation/signin.html', context_dict)
		if not 'password' in request.POST:
			context_dict['login_error_message'] = 'Please enter your password.'
			context_dict['next'] = request.GET.get('next', '')
			return render(request, 'simplenation/signin.html', context_dict)

		email_or_username = request.POST['email_or_username']
		password = request.POST['password']

		if simplenation_email_validation(email_or_username):
			email = request.POST['email_or_username']
			user_by_email = User.objects.get(email=email)
			username = user_by_email.username
			user = authenticate(username=username, password=password)
		elif simplenation_username_validation(email_or_username):
			username = request.POST['email_or_username']
			user = authenticate(username=username, password=password)
		else:
			context_dict['login_error_message'] = 'Invalid username/email or password.'
			context_dict['next'] = request.GET.get('next', '')
			return render(request, 'simplenation/signin.html', context_dict)

		
		if user:
			if user.is_active:
				login(request,user)
				if request.POST["next"] is not "":
					return HttpResponseRedirect(request.POST["next"])
				else:
					return HttpResponseRedirect('/simplenation/')

			else:
				messages.error(request, 'Your account has been disabled.')
				context_dict['login_error_message'] = 'Your account has been disabled.'
		else:
			messages.error(request, 'Invalid username or password.')
			context_dict['login_error_message'] = 'Invalid username or password.'

	context_dict['next'] = request.GET.get('next', '')
		
	return render(request, 'simplenation/signin.html', context_dict) 


@login_required
def send_email_confirmation(request):

	context_dict = {}
	email = request.user.email
	salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
	account_deletion_key = hashlib.sha1(salt+email).hexdigest()

	email_data = {
		'email': email,
		'domain': request.META['HTTP_HOST'],
		'site_name': SITE_NAME,
		'account_deletion_key': account_deletion_key,
		'receiver_username': request.user.username,
		'site_email': EMAIL_HOST_USER,
		'protocol': 'http',
	}
	subject_template_name='simplenation/registration_notification_subject.txt'
	email_template_name='simplenation/registration_notification_email.html'
	
	if not send_email(email_data, subject_template_name, email_template_name):
		context_dict['success'] = False
		return HttpResponse(json.dumps(context_dict), content_type='application/json')

	context_dict['success'] = True
	return HttpResponse(json.dumps(context_dict), content_type='application/json')


@login_required
def user_logout(request):
	
	logout(request)
	
	return HttpResponseRedirect('/simplenation/')


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
						'site_name': SITE_NAME,
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
					send_mail(subject, email, EMAIL_HOST_USER , [user.email], fail_silently=False)

				result = self.form_valid(form)
				messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
				return result

			result = self.form_invalid(form)
			messages.error(request, 'No user is found with this email address')
			return result

		else:
			associated_users= User.objects.filter(username=data)
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': request.META['HTTP_HOST'],
						'site_name': SITE_NAME,
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
					send_mail(subject, email, EMAIL_HOST_USER , [user.email], fail_silently=False)

				result = self.form_valid(form)
				messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
				return result

			result = self.form_invalid(form)
			messages.error(request, 'No user is associated with this username')
			return result

		messages.error(request, 'Invalid Input')
		return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
	template_name = "simplenation/password_set_new.html"
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



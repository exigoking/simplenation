from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.models import Term, Author, Definition, Like, Report, Favourite
from simplenation.forms import UserForm, ProfileForm, DefinitionForm, TermForm, PasswordResetRequestForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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



#@login_required
def profile(request, profile_name_slug):
	context_dict = {}

	try:
		author = Author.objects.get(slug=profile_name_slug)
		explanations = Definition.objects.filter(author = author).order_by('-likes')

		favorees = Favourite.objects.favorees_for_user(author.user)

		if not Favourite.objects.is_favoree(request.user, author.user):
			context_dict['favor_button_text'] = "Add to favourites"
		else:
			context_dict['favor_button_text'] = "Remove from favourites"

		context_dict['explanations'] = explanations
		context_dict['author'] = author
		context_dict['profile_name'] = author.user.username
		context_dict['profile_email'] = author.user.email
		context_dict['profile_bio'] = author.bio

		if favorees:
			context_dict['favorees'] = favorees
		else:
			pass

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



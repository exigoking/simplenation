from django import forms
from simplenation.models import Term, Author, Definition, Picture
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm


class TermForm(forms.ModelForm):
	name = forms.TextInput(attrs={'placeholder':'Article name...'})
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Term
		fields = ('name',)

class DefinitionForm(forms.ModelForm):
	body = forms.CharField(error_messages = {
								'required': (""),
								}, max_length = 4096,label = '', widget=forms.Textarea(attrs={'placeholder':'Explain in your own words...', 'id':'exp_input', 'cols':'92', 'rows':'7','class':'w-input post-input'}))
	class Meta:
		model = Definition
		fields = ('body',)
 

class UserForm(forms.ModelForm):
	
	username = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder':'Enter username...'})
		)
	email = forms.EmailField(widget = forms.TextInput(attrs={'placeholder':'Enter email...'}))
	password1 = forms.CharField(error_messages = {
								'password_mismatch': ("Passwords don't match."),
								'required':("Please enter password."),
								},
								widget=forms.PasswordInput(attrs={'placeholder':'New password...'}))
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1',)

	def clean_email(self):
	    email = self.cleaned_data["email"]
	    try:
	        User._default_manager.get(email=email)
	    except User.DoesNotExist:
	        return email
	    raise forms.ValidationError('We have someone with this email already.')

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
		    user.save()
		return user


	
class ProfileForm(forms.ModelForm):
	picture = forms.ImageField(required = False)
	class Meta:
		model = Author
		fields = ('picture',)

class NewProfileForm(RegistrationForm):
	picture = forms.ImageField(label="Profile picture", required = False)
	
	
class PasswordResetRequestForm(forms.Form):
	email_or_username = forms.CharField(max_length=254, widget = forms.TextInput(attrs={'placeholder':'Email or Username...'}))

class SetPasswordForm(forms.Form):
	error_messages = {
		'password_mismatch': ("The two password fields didn't match."),
		'required':("Please enter password."),
	}
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'New password...'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm password...'}))

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code='password_mismatch',
					)
		return password2

class PictureForm(forms.ModelForm):
	pictures = forms.ImageField()
	class Meta:
		model = Picture
		fields = ('pictures',)

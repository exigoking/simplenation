from django import forms
from simplenation.models import Term, Author, Definition
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm

class TermForm(forms.ModelForm):
	name = forms.TextInput(attrs={'placeholder':'Enter the term...'})
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Term
		fields = ('name',)

class DefinitionForm(forms.ModelForm):
	body = forms.CharField(max_length = 512, widget=forms.Textarea(attrs={'placeholder':'Explain in your own words...'}))
	class Meta:
		model = Definition
		fields = ('body',)
 

class UserForm(UserCreationForm):
	username = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder':'Enter username...'})
		)
	email = forms.EmailField(widget = forms.TextInput(attrs={'placeholder':'Enter email...'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def clean_email(self):
	    email = self.cleaned_data["email"]
	    try:
	        User._default_manager.get(email=email)
	    except User.DoesNotExist:
	        return email
	    raise forms.ValidationError('duplicate email')

	
class ProfileForm(forms.ModelForm):
	bio = forms.CharField(required = False)
	class Meta:
		model = Author
		fields = ('picture','bio')

class NewProfileForm(RegistrationForm):
	picture = forms.ImageField(label="Profile picture", required = False)
	bio = forms.CharField(required = False)
	
class PasswordResetRequestForm(forms.Form):
	email_or_username = forms.CharField(max_length=254, widget = forms.TextInput(attrs={'placeholder':'Email or Username...'}))

class SetPasswordForm(forms.Form):
	error_messages = {
		'password_mismatch': ("The two password fields didn't match."),
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



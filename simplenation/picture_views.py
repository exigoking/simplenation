from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import get_user_model
from simplenation.models import Picture, Definition
from simplenation.forms import PictureForm
import json
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def add_picture(request, explanation_id):
	"""
	Add picture to definition. 
	"""
	context_dict = {}
	
	if request.method == "POST":

		picture_form = PictureForm(request.POST, request.FILES)
		definition = Definition.objects.get(id = explanation_id)

		if picture_form.is_valid():
			picture = picture_form.cleaned_data['pictures']
			added_picture = Picture(definition = definition, image = picture, image_thumbnail = picture, term=definition.term, to_add = True)
			added_picture.save()
			context_dict['success'] = True
			context_dict['user'] = request.user

			if added_picture:
				context_dict['picture'] = added_picture
			else:
				context_dict['picture'] = None

			context_dict['explanation'] = definition
		else:
			context_dict['success'] = False
			context_dict['no_success_message'] = "Wrong file type."
			return HttpResponse(json.dumps(context_dict), content_type = 'application/json')
				

	else:
		context_dict['success'] = False
		context_dict['no_success_message'] = "Invalid form."
		return HttpResponse(json.dumps(context_dict), content_type = 'application/json')

	html = render_to_string('simplenation/add_picture.html', context_dict)
	return HttpResponse(html)



@login_required
def remove_picture(request):
	"""
	Remove picture from explanation.
	"""
	params=json.loads(request.body)

	picture_id = params['picture_id']
	context_dict = {}
	context_dict['user'] = request.user

	if request.method == "POST":
		picture = Picture.objects.get(id = picture_id)

		if picture:
			definition = picture.definition
			picture.to_delete = True
			picture.save()
			pictures = Picture.objects.filter(definition = definition)
			if pictures:
				context_dict['pictures'] = pictures
			else:
				context_dict['pictures'] = None
			context_dict['explanation'] = definition
			
		else:
			return HttpResponse("Already removed from pictures.")

	else:
		context_dict['success'] = False
		context_dict['no_success_message'] = "Invalid form."

	html = render_to_string('simplenation/pictures.html', context_dict)
	return HttpResponse(html)


@login_required
def cancel_edition(request):
	params=json.loads(request.body)

	explanation_id = params['explanation_id']
	context_dict = {}

	context_dict['user'] = request.user


	if request.method == "POST":
		definition = Definition.objects.get(id = explanation_id)
		pictures = Picture.objects.filter(definition = definition)
		if pictures:
			for picture in pictures:
				if picture.to_delete:
					picture.to_delete = False
					picture.save()
				if picture.to_add:
					picture.delete()

		pictures = Picture.objects.filter(definition = definition)
		context_dict['pictures'] = pictures
		context_dict['explanation'] = definition

	else:
	    return HttpResponse("Invalid Form.")

	html = render_to_string('simplenation/pictures_pressed_cancel.html', context_dict)
	return HttpResponse(html)

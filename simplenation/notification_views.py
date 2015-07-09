from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from simplenation.models import Challenge, Term, Notification
import json
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from simplenation.addons import last_posted_date, profanityFilter


@login_required
def recent_notifications(request):

	"""
	return 20 last notifications for the user.
	"""
	context_dict = {}
	recent_notifications = Notification.objects.recent_notifications(request.user)

	if recent_notifications:
			Notification.objects.filter(receiver = request.user, seen = False).update(seen = True)
			for notification in recent_notifications:
				notification.humanized_created_at = last_posted_date(notification.created_at)

			context_dict['notifications'] = recent_notifications

	else:
		context_dict['notifications'] = None

	
	return render(request, 'simplenation/notifications.html', context_dict)

@login_required
def are_new_notifications(request):

	"""
	Checks whether there are new notifications or not.
	"""

	json_data = {}

	unseen_notifications = Notification.objects.unseen_notifications(request.user)

	if unseen_notifications:
		json_data['notification_flag'] = True
		json_data['num_of_unseen_notifications'] = unseen_notifications.count()

	else:
		json_data['notification_flag'] = False
		json_data['num_of_unseen_notifications'] = None
	
	return HttpResponse(json.dumps(json_data), content_type='application/json')
from django.shortcuts import render_to_response, get_object_or_404, redirect
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

@login_required
def challenge(request):
    """
    Challenging a user to explain a term.
    """
    params=json.loads(request.body)

    challengee_id = params['challengee_id']
    term_id = params['term_id']

    challengee = get_object_or_404(get_user_model(), id=challengee_id)

    term = Term.objects.get(id = term_id)

    if request.method == "POST":
        if not Challenge.objects.been_challenged(request.user, challengee, term):
            challenge = Challenge()
            challenge.challenger = request.user
            challenge.challengee = challengee
            challenge.subject = term
            challenge.save()
            Notification(typeof = 'challenge_notification', sender = request.user, receiver = challengee, term = term).save()


        else:
            pass
    else:
        HttpResponse("Invalid Form.")

    return HttpResponse("You have challenged "+ challengee.username + " to explain " + term.name)
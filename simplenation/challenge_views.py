from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from simplenation.models import Challenge, Term, Notification, Author
import json
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from djangobook.settings import SITE_NAME
from simplenation.addons import send_email
from django.contrib.auth import get_user_model

@login_required
def challenge(request):
    """
    Challenging a user to explain a term.
    """
    params=json.loads(request.body)
    context_dict = {}

    challengee_id = params['challengee_id']
    term_id = params['term_id']

    challengee = get_object_or_404(get_user_model(), id=challengee_id)
    term = Term.objects.get(id = term_id)

    context_dict['term_id'] = term.id
    context_dict['term_name'] = term.name
    context_dict['challengee_id'] = challengee.id
    context_dict['challengee_name'] = challengee.username


    if request.method == "POST":
        if not Challenge.objects.been_challenged(request.user, challengee, term):
            if request.user.id != challengee.id:
                challenge = Challenge()
                challenge.challenger = request.user
                challenge.challengee = challengee
                challenge.subject = term
                challenge.save()
                context_dict['success'] = True

                Notification(typeof = 'challenge_notification', sender = request.user, receiver = challengee, term = term).save()

                email_data = {
                        'email': challengee.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': SITE_NAME,
                        'receiver': challengee,
                        'sender': request.user,
                        'term': term,
                        'protocol': 'http',
                }
                subject_template_name='simplenation/challenge_notification_subject.txt'
                email_template_name='simplenation/challenge_notification_email.html'
                send_email(email_data, subject_template_name, email_template_name)


            else:
                context_dict['success'] = False
                context_dict['no_success_message'] = "Can't challenge yourself."


        else:
            context_dict['success'] = False
            context_dict['no_success_message'] = 'Has already been challenged.'
    else:
        context_dict['success'] = False
        context_dict['no_success_message'] = 'Invalid form request.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

@login_required
def challengee_list(request):
    """
    Challenging a user to explain a term.
    """
    params=json.loads(request.body)
    context_dict = {}

    term_id = params['term_id']

    term = Term.objects.get(id = term_id)

    context_dict['term_id'] = term.id
    context_dict['term_name'] = term.name

    challengee_list = []

    if request.method == "POST":

        challenges = Challenge.objects.filter(challenger=request.user, subject=term)
        if challenges:
            
            for challenge in challenges:
                challengee = {}
                challengee['id'] = challenge.challengee.id
                challengee['name'] = challenge.challengee.username
                challengee_list.append(challengee)

            context_dict['challengee_list'] = challengee_list

        else:
            context_dict['success'] = False
            context_dict['no_success_message'] = 'None was challenged.'
    else:
        context_dict['success'] = False
        context_dict['no_success_message'] = 'Invalid form request.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")



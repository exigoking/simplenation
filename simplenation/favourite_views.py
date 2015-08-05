from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from simplenation.models import Favourite, Term, Author
import json
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def update_favoree_list(request):
    """
    Update list of favourites.
    """
    context_dict = {}
    params = json.loads(request.body)
    term_id = params['term_id']
    context_dict['success'] = True
    if term_id:
        term = Term.objects.get(id = term_id)

    if term:
        context_dict['term'] = term

    if request.user.id:
        favorees = Favourite.objects.favorees_for_user(request.user)
        top_contributors = list(Author.objects.order_by('-score')[:50])
        if favorees:
            favorees_of_favorees = []
            for favoree in favorees:
                favorees_of_favorees.extend(list(Favourite.objects.favorees_for_user(favoree)))
                if top_contributors:
                    if favoree.author in top_contributors:
                        top_contributors.remove(favoree.author)

            if favorees_of_favorees:
                favorees_of_favorees = list(set(favorees_of_favorees) - set(favorees))

            if request.user in favorees_of_favorees:
                favorees_of_favorees.remove(request.user)

            context_dict['favourites'] = favorees
            if favorees_of_favorees:
                for favoree in favorees_of_favorees:
                    if favoree.author in top_contributors:
                        top_contributors.remove(favoree.author)
                context_dict['favourites_of_favourites'] = favorees_of_favorees

        if top_contributors:
            if request.user.author in top_contributors:
                top_contributors.remove(request.user.author)
            context_dict['top_contributors'] = top_contributors
                
    else:
        context_dict['success'] = False
        context_dict['no_success_message'] = "No user associated with request."

    html = render_to_string('simplenation/update_favoree_list.html', context_dict)
    return HttpResponse(html)

@login_required
def add_favoree(request):
    """
    Add user to favourites.
    """
    context_dict = {}
    params=json.loads(request.body)

    favoree_id = params['favoree_id']

    favoree = get_object_or_404(get_user_model(), id=favoree_id)
    context_dict["favoree_id"] = favoree.id
    context_dict["favoree_name"] = favoree.username

    if request.method == "POST":
        if not Favourite.objects.is_favoree(request.user, favoree):
            if request.user.id != favoree.id:
                favourite = Favourite()
                favourite.favoror = request.user
                favourite.favoree = favoree
                favourite.save()
                context_dict["success"] = True
            else:
                context_dict["success"] = False
                context_dict["no_success_message"] = "Can't add yourself to favorites."
        else:
            context_dict["success"] = False
            context_dict["no_success_message"] = "Has been added to favourites."
    else:
        context_dict["success"] = False
        context_dict["no_success_message"] = "Invalid Form."

    return HttpResponse(json.dumps(context_dict), content_type="application/json")


@login_required
def remove_favoree(request):
    """
    Remove user from favourites.
    """
    context_dict = {}
    params=json.loads(request.body)

    favoree_id = params['favoree_id']

    favoree = get_object_or_404(get_user_model(), id=favoree_id)
    context_dict["favoree_id"] = favoree.id
    context_dict["favoree_name"] = favoree.username

    if request.method == "POST":
        favourite = Favourite.objects.get(favoror = request.user, favoree = favoree)
        if favourite:
            if favoree.id != request.user.id:
                favourite.delete()
                context_dict["success"] = True
            else:
                context_dict["success"] = False
                context_dict["no_success_message"] = "Can't remove yourself from favorites."

        else:
            context_dict["success"] = False
            context_dict["no_success_message"] = "Has been added to favourites."
            
    else:
        context_dict["success"] = False
        context_dict["no_success_message"] = "Invalid Form."

    return HttpResponse(json.dumps(context_dict), content_type="application/json")






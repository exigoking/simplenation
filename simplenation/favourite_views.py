from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from simplenation.models import Favourite
import json
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect

@login_required
def list_favorees(request):
    """
    Lists friends of currently logged user.
    """
    favorees = Favourite.objects.favorees_for_user(request.user)
    return render_to_response('simplenation/favorees_list.html',
                              {'favorees': favorees},
                              context_instance=RequestContext(request))


@login_required
def list_favorees_another_user(request, username):
    """
    Lists friends of user friend.
    """

    user = get_object_or_404(get_user_model(), username=username)

    favorees = Favourite.objects.favorees_for_user(user)
    return render_to_response('friends/friends_of_friend.html',
                              {'favorees': favorees,
                               'friend': user},
                              context_instance=RequestContext(request))


@login_required
def add_favoree(request):
    """
    Add user to favourites.
    """
    params=json.loads(request.body)

    favoree_id = params['favoree_id']

    favoree = get_object_or_404(get_user_model(), id=favoree_id)

    if request.method == "POST":
        if not Favourite.objects.is_favoree(request.user, favoree):
            favourite = Favourite()
            favourite.favoror = request.user
            favourite.favoree = favoree
            favourite.save()
        else:
            pass
    else:
        return HttpResponse("Invalid Form.")

    return HttpResponse("Added to favourites.")


@login_required
def remove_favoree(request):
    """
    Remove user from favourites.
    """
    params=json.loads(request.body)

    favoree_id = params['favoree_id']

    favoree = get_object_or_404(get_user_model(), id=favoree_id)

    if request.method == "POST":
        favourite = Favourite.objects.get(favoror = request.user, favoree = favoree)
        if favourite:
            favourite.delete()
        else:
            return HttpResponse("Already removed from favourites.")
            
    else:
        return HttpResponse("Invalid Form.")

    return HttpResponse("Removed from favourites.")






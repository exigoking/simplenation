"""
WSGI config for djangobook project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangobook.settings")


# add the hellodjango project path into the sys.path
sys.path.append('Users/timurmalgazhdarov/Documents/djangobook')

# add the virtualenv site-packages path to the sys.path
sys.path.append('Users/timurmalgazhdarov/Documents/VirtualEnvs/venv-python2.7-django/lib/python2.7/site-packages/')



from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf.urls import patterns, include, url
from django.contrib import admin
from djangobook.views import hello
from djangobook.settings import STATIC_ROOT
from simplenation.forms import NewProfileForm
from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',

    url(r'^simplenation/', include('simplenation.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : MEDIA_ROOT}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root' : STATIC_ROOT}),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)

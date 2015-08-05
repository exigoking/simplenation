from django.conf.urls import patterns, include, url
from django.contrib import admin
from djangobook.views import hello, redirect_from_simplenation
from djangobook.settings import MEDIA_ROOT, STATIC_ROOT
from simplenation.forms import NewProfileForm
from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',

    url(r'^', include('simplenation.urls')),
    url(r'^simplenation/', redirect_from_simplenation, name="redirect_from_simplenation"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : MEDIA_ROOT}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root' : STATIC_ROOT}),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)

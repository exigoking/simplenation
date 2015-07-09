from django.conf.urls import patterns, include, url
from django.contrib import admin
from djangobook.views import hello
from djangobook.settings import MEDIA_ROOT, STATIC_ROOT
from simplenation.forms import NewProfileForm
from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangobook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^simplenation/', include('simplenation.urls')),
    url(r'^snippets_app/', include('snippets.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : MEDIA_ROOT}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root' : STATIC_ROOT}),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'accounts/register/$', 
    #     RegistrationView.as_view(form_class = NewProfileForm), 
    #     name = 'registration_register', kwargs=dict(extra_context={'next_page': '/simplenation/'})),
    # url(r'^accounts/', include('registration.backends.default.urls')),
)

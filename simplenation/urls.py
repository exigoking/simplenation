from django.conf.urls import patterns, url
from djangobook import views
from simplenation import views
from simplenation.user_views import PasswordResetRequestView, PasswordResetConfirmView
from simplenation import general_views, user_views, term_views, explanation_views, favourite_views, challenge_views, notification_views, picture_views

urlpatterns = patterns('',
	# Calls to General Controller
	url(r'^$', general_views.index, name = 'index'),
	url(r'^search/', general_views.search, name = 'search'),
	url(r'^autocomplete_search/$', general_views.autocomplete_search, name = 'autocomplete_search'),
	url(r'^autocomplete_tag_search/$', general_views.autocomplete_tag_search, name = 'autocomplete_tag_search'),

	# Calls to User Controller
	url(r'^registration_form/$', user_views.register, name='register'),
	url(r'^signin/$', user_views.user_login, name='signin'),
	url(r'^signout/$', user_views.user_logout, name='signout'),
	url(r'^profile/(?P<profile_name_slug>[\w\-]+)/$', user_views.profile, name = 'profile'),
	url(r'^profile/(?P<profile_name_slug>[\w\-]+)/edit_profile/$', user_views.edit_profile, name='edit_profile'),
	url(r'^email_confirmation/(?P<account_deletion_key>\w+)/$', user_views.email_confirmation, name='email_confirmation'),
	url(r'^reset_password/$', PasswordResetRequestView.as_view(), name="reset_password"),
	url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
	url(r'^password_sent_confirmation/$', user_views.password_sent_confirmation, name="password_sent_confirmation"),
	url(r'^send_email_confirmation/$', user_views.send_email_confirmation, name="send_email_confirmation"),

	# Calls to Term Controller
	url(r'^term/(?P<term_name_slug>[\w\-]+)/$', term_views.term, name = 'term'),
	url(r'^add_term/$', term_views.add_term, name='add_term'),
	url(r'^add_tags_to_term/$', term_views.add_tags_to_term, name='add_tags_to_term'),
	url(r'^tag_select/$', term_views.tag_select, name='tag_select'),
	url(r'^tag_deselect/$', term_views.tag_deselect, name='tag_deselect'),
	url(r'^search_tags/$', term_views.search_tags, name='search_tags'),
	url(r'^single_tag_view/(?P<tag_slug>[\w\-]+)/$', term_views.single_tag_view, name='single_tag_view'),

	
	# Calls to Explanation Controller
	url(r'^edit_exp/$', explanation_views.edit_exp, name='edit_exp'),
	url(r'^add_like/$', explanation_views.add_like, name='add_like'),
	url(r'^remove_like/$', explanation_views.remove_like, name='remove_like'),
	url(r'^report_explanation/$', explanation_views.report_explanation, name='report_explanation'),

	# Calls to Favorites Controller
	url(r'^add_favoree/$', favourite_views.add_favoree, name='add_favoree'),
	url(r'^remove_favoree/$', favourite_views.remove_favoree, name='remove_favoree'),
	url(r'^update_favoree_list/$', favourite_views.update_favoree_list, name='update_favoree_list'),

	# Calls to Challenge Controller
	url(r'^challenge/$', challenge_views.challenge, name='challenge'),
	url(r'^challengee_list/$', challenge_views.challengee_list, name='challengee_list'),

	# Calls to Notification Controller
	url(r'^are_new_notifications/$', notification_views.are_new_notifications, name='are_new_notifications'),
	url(r'^recent_notifications/$', notification_views.recent_notifications, name='recent_notifications'),

	# Calls to Picture Controller
	url(r'^add_picture/(?P<explanation_id>[\w\-]+)/$', picture_views.add_picture, name='add_picture'),
	url(r'^remove_picture/$', picture_views.remove_picture, name='remove_picture'),
	url(r'^cancel_edition/$', picture_views.cancel_edition, name='cancel_edition'),

 
)

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from simplenation.addons import last_posted_date
from taggit.managers import TaggableManager
from taggit.models import Tag
from registration.signals import user_registered
from django.db.models import Count
from simplenation.managers import FavouriteManager, ChallengeManager, NotificationManager, LikeManager, TermVoteManager
from django.utils.translation import ugettext_lazy as _
from djangobook import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.decorators import login_required


class Author(models.Model):
	"""
    An author is a profile for a user that has registered @simplenation.
    """
	user = models.OneToOneField(User)
	bio = models.CharField(max_length=1024)
	picture = ProcessedImageField(upload_to='profile_images', default = 'profile_images/default_profile_picture.png', processors=[ResizeToFill(400, 400)], format='JPEG', options={'quality': 100})
	slug = models.SlugField(unique=True)
	account_deletion_key = models.CharField(max_length = 64, blank = True)
	score = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	rank = models.IntegerField(default=9999999)
	num_of_likes = models.IntegerField(default=0)
	active = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.username)
		super(Author, self).save(*args, **kwargs)

	def ranking(self):
		aggregate = Author.objects.filter(score__gt=self.score).aggregate(ranking=Count('score'))
		return aggregate['ranking'] + 1

	def has_favorites(self):
		if self.user.favorees.count() > 0:
			return True
		else: 
			return False
	def favorite_list(self):
		return self.user.favorees.all()

	def favorite_count(self):
		return self.user.favorees.count()

	def __unicode__(self):
		return self.user.username



class Term(models.Model):
	"""
    A term is a word that needs a definition or definitions.
    A term can be created by any registered user @simplenation.
    """
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	author = models.ForeignKey(Author, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	tags = TaggableManager(blank=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		name_elements = self.name.split()
		cleaned_name_elements = []
		if name_elements:
			for element in name_elements:
				if not element.isupper():
					element = element.title()
				cleaned_name_elements.append(element)
			cleaned_name = " ".join(cleaned_name_elements)
		else:
			if self.name.isupper():
				cleaned_name = self.name
			else:
				cleaned_name = self.name.title()

		self.name = cleaned_name
		super(Term, self).save(*args, **kwargs)

	def iterable_tags(self):
		return self.tags.all()
	def has_explanations(self):
		if self.definition_set.count() > 0:
			return True
		else:
			return False
	def number_of_explanations(self):
		return self.definition_set.count()
	def sorted_by_number_of_views_descending(self):
		return self.order_by('-views') 

	def sorted_by_number_of_views(self):
		return self.order_by('views')

	def sorted_by_number_of_explanations(self):
		return self.annotate(exp_count=Count('definition')).order_by('exp_count')

	def sorted_by_number_of_explanations_descending(self):
		return self.annotate(exp_count=Count('definition')).order_by('-exp_count')

	def upvoted(self, user):
		voters = []
		for vote in self.votes.all():
			if vote.upvote:
				voters.append(vote.user)
		if user in voters:
			return True
		else:
			return False

	def downvoted(self, user):
		voters = []
		for vote in self.votes.all():
			if vote.downvote:
				voters.append(vote.user)
		if user in voters:
			return True
		else:
			return False

	def upvote_count(self):
		return self.upvotes

	def downvote_count(self):
		return self.downvotes
	
	def __unicode__(self):
		return self.name

class TermVote(models.Model):
	"""
    A vote is to rank a term.
    """
	user = models.ForeignKey(User)
	term = models.ForeignKey(Term, related_name='votes')
	upvote = models.BooleanField(default=False)
	downvote = models.BooleanField(default=False)

	objects = TermVoteManager()

	def __unicode__(self):
		return self.user.username



class Definition(models.Model):
	"""
   	A definition is required to describe a term.
    A definition can be created by any registerd user @simplenation.
    A term can have multiple definitions.
    """
	author = models.ForeignKey(Author, null=True)
	term = models.ForeignKey(Term, null=True)
	body = models.TextField(max_length=4096)
	likes = models.IntegerField(default=0)
	post_date = models.DateTimeField(auto_now_add=True)	
	last_posted = models.CharField(max_length=128, blank=True)
	like_text = models.CharField(max_length=128, default='Like')
	times_reported = models.IntegerField(default=0)
	reporter = models.IntegerField(default=0)


	def __unicode__(self):
		return self.term.name



class Picture(models.Model):
	definition=models.ForeignKey(Definition,related_name='pictures_for_explanation')
	term=models.ForeignKey(Term,related_name='pictures_for_term', null=True)
	image=models.ImageField(upload_to="pictures/")
	image_thumbnail = ProcessedImageField(upload_to="thumbnail_pictures/",processors=[ResizeToFill(300, 300)],format='JPEG',options={'quality': 100})
	deleted=models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	to_delete = models.BooleanField(default=False)
	to_add = models.BooleanField(default=False)

	def __unicode__(self):
		return 'Picture with id {0}'.format(self.id)


class Like(models.Model):
	"""
    A like is to rank a definition for filtering out best definitions.
    """
	user = models.ForeignKey(User)
	definition = models.ForeignKey(Definition)
	liked = models.BooleanField(default=False)
	upvote = models.BooleanField(default=False)
	downvote = models.BooleanField(default=False)

	objects = LikeManager()

	def __unicode__(self):
		return self.user.username


class Report(models.Model):
	"""
    A report is to notify @simplenation admins about inappropriate definitions.
    """
	user = models.ForeignKey(User)
	definition = models.ForeignKey(Definition)
	reported = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username



class Favourite(models.Model):
    """
    A Favourite is a bi-directional association between two authors who
    have both agreed to the association.
    """

    favoror = models.ForeignKey(User, verbose_name=_("favoror"), related_name="_unused_")
    favoree = models.ForeignKey(User, verbose_name=_("favoree"), related_name="favorees")
    added = models.DateTimeField(_("added"), auto_now_add=True)

    objects = FavouriteManager()

    def __unicode__(self):
		return self.favoror.username


class Challenge(models.Model):
	"""
    A Challenge is a three-directional association between two authors and 
    a term.
    """

	challenger = models.ForeignKey(User, verbose_name=_("challenger"), related_name = "challengers")
	subject = models.ForeignKey(Term, verbose_name=_("subject"), related_name="terms")
	challengee = models.ForeignKey(User, verbose_name=_("challengee"), related_name = "challengees")
	added = models.DateTimeField(_("added"), auto_now_add=True)

	objects = ChallengeManager()

	def __unicode__(self):
		return self.challenger.username

class Notification(models.Model):
	"""
    A Notification to let users know about updates @simplenation.
    """
	typeof=models.CharField(max_length=140,blank=True,default='')
	receiver=models.ForeignKey(User,related_name='notifications')
	sender=models.ForeignKey(User,related_name='sent_notifications')
	term=models.ForeignKey(Term,related_name='term_notifications',null=True)
	definition=models.ForeignKey(Definition,related_name='event_notifications',null=True)
	created_at = models.DateTimeField(auto_now_add=True)	
	seen = models.BooleanField(default=False)
	humanized_created_at = models.CharField(max_length=128, blank=True)

	objects = NotificationManager()

	def __unicode__(self):
		return self.typeof


class Session(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	tags = TaggableManager()


class PressedTag(models.Model):
    name = models.CharField(max_length=200)
    session = models.ForeignKey(Session, related_name='pressed_tags')

    def __unicode__(self):
		return self.id

    def setname(self, x):
        self.name = x

    def getname(self, x):
        return self.name




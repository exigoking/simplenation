from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from simplenation.addons import last_posted_date
from taggit.managers import TaggableManager
from registration.signals import user_registered
from django.db.models import Count
from simplenation.managers import FavouriteManager, ChallengeManager, NotificationManager, LikeManager
from django.utils.translation import ugettext_lazy as _
from djangobook import settings


class Term(models.Model):
	"""
    A term is a word that needs a definition or definitions.
    A term can be created by any registered user @simplenation.
    """
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	tags = TaggableManager()
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		self.name = self.name.title()
		super(Term, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.name

class Author(models.Model):
	"""
    An author is a profile for a user that has registered @simplenation.
    """
	user = models.OneToOneField(User)
	bio = models.CharField(max_length=1024)
	picture = models.ImageField(upload_to='profile_images', default = 'profile_images/default_profile_picture.png')
	slug = models.SlugField(unique=True)
	account_deletion_key = models.CharField(max_length = 64, blank = True)
	score = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	rank = models.IntegerField(default=9999999)
	num_of_likes = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.username)
		super(Author, self).save(*args, **kwargs)

	def ranking(self):
		aggregate = Author.objects.filter(score__gt=self.score).aggregate(ranking=Count('score'))
		return aggregate['ranking'] + 1

	def __unicode__(self):
		return self.user.username
	

class Definition(models.Model):
	"""
   	A definition is required to describe a term.
    A definition can be created by any registerd user @simplenation.
    A term can have multiple definitions.
    """
	author = models.ForeignKey(Author)
	term = models.ForeignKey(Term)
	body = models.TextField(max_length=512)
	likes = models.IntegerField(default=0)
	post_date = models.DateTimeField(auto_now_add=True)	
	last_posted = models.CharField(max_length=128, blank=True)
	like_text = models.CharField(max_length=128, default='Like')
	times_reported = models.IntegerField(default=0)
	reporter = models.IntegerField(default=0)


	def __unicode__(self):
		return self.term.name


class Like(models.Model):
	"""
    A like is to rank a definition for filtering out best definitions.
    """
	user = models.ForeignKey(User)
	definition = models.ForeignKey(Definition)
	liked = models.BooleanField(default=False)

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






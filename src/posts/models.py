from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.
#Post.objects.all is also a manager
#Post.objects.create(user=user, title="Some title", ..... ) is also a manager

class PostManager(models.Manager):
	"""docstring for PostManager"""
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
		
		
class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	image = models.FileField(null=True, blank=True)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	objects = PostManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id": self.id})
		# return "/posts/%s/" %(self.id)


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from unidecode import unidecode
import os
from users.models import Profile
from django.urls import reverse


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "challenges/%s%s" % (now.strftime("%Y/%m/%Y%m%d%H%M%S"), filename_ext.lower(),)

def upload_video(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "videos/%s%s" % (now.strftime("%Y/%m/%Y%m%d%H%M%S"), filename_ext.lower(),)

# Create your models here.
class Challenge(models.Model):
	ANY = 'A'
	MALE = 'M'
	FEMALE = 'F'
	GENDER = [
		(ANY, 'Any'),
		(MALE, 'Male'),
		(FEMALE, 'Female')

	]
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True, null=True)
	task = models.TextField(max_length=2000)
	criteria = models.TextField(max_length=2000)
	gender = models.CharField(max_length=1, choices=GENDER, default=ANY)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	user = models.ForeignKey(User, related_name='challenges_created', on_delete=models.CASCADE)
	challenge_image = models.ImageField(upload_to=upload_to, null=True)


	class Meta:
		ordering = ('-start_time',)
		verbose_name = 'Challenge'
		verbose_name_plural = 'Challenges'

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(unidecode(self.title))
		super(Challenge, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('challenge', args=[self.slug])

class Joined(models.Model):
    profile = models.ForeignKey(Profile, related_name='join_from_set', null=True, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, related_name='join_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} joined {}'.format(self.profile.get_screen_name(), self.challenge)


class Invitation(models.Model):
	inv_from = models.ForeignKey(User, related_name='inv_from', on_delete=models.CASCADE)
	inv_to = models.ForeignKey(User, related_name='inv_to', on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, related_name='inv_challenge', on_delete=models.CASCADE)

	def __str__(self):
		return '{} invited {} to {}'.format(self.inv_from, self.inv_to, self.challenge.title)

class FinishChallenge(models.Model):
	score = models.IntegerField()
	video = models.FileField(upload_to=upload_video)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	def __str__(self):
		return '{} finished challenge {}'.format(self.profile.get_screen_name(), self.challenge.title)

from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
import urllib
import hashlib
import os.path
from django.db.models.signals import post_save
from django.utils.timezone import now as timezone_now
from activities.models import Notification


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "profile/%s%s" % (
        now.strftime("%Y/%m/%Y%m%d%H%M%S"),
        filename_ext.lower(),)


def upload_back(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "profile/back_image/%s%s" % (
        now.strftime("%Y/%m/%Y%m%d%H%M%S"),
        filename_ext.lower(),)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)
    back_image = models.ImageField(upload_to=upload_back, null=True, blank=True)
    joined_challenges = models.ManyToManyField('challenges.Challenge', through='challenges.Joined')
    # reputation = models.IntegerField(default=0)
    # language = models.CharField(max_length=5, default='en')

    class Meta:
        db_table = 'auth_profile'

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)

        return url

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def notify_invited(self, challenge, user):
        if self.user != user:
            Notification(notification_type=Notification.INVITED,
                         from_user=self.user, to_user=user,
                         challenge=challenge).save()

    def unotify_invited(self, challenge, user):
        if self.user != user:
            Notification.objects.filter(notification_type=Notification.INVITED,
                         from_user=self.user, to_user=user,
                         challenge=challenge).delete()

    def notify_followed(self, user):
        if self.user != user:
            Notification(notification_type=Notification.FOLLOWED,
                         from_user=self.user, to_user=user,
                         user=user).save()

    def unotify_followed(self, user):
        if self.user != user:
            Notification.objects.filter(notification_type=Notification.FOLLOWED,
                         from_user=self.user, to_user=user,
                         user=user).delete()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


# Add following field to User dynamically
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
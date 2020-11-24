from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.html import escape
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    parent = models.ForeignKey('Action', null=True, blank=True, on_delete=models.CASCADE)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    date = models.DateTimeField(auto_now_add=True,
                                db_index=True)

    class Meta:
        ordering = ('-date',)

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Action.objects.filter(parent=None, id__lte=from_feed)
        else:
            feeds = Action.objects.filter(parent=None)
        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Action.objects.filter(parent=None, id__gt=feed)
        return feeds


class Activity(models.Model):
    JOINED = 'J'
    SCORE = 'S'
    ACTIVITY_TYPES = (
        (JOINED, 'Joined'),
        (SCORE, 'Scored'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    challenge = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity_type


# def save(self, *args, **kwargs):
#        super(Activity, self).save(*args, **kwargs)
#        if self.activity_type == Activity.FAVORITE:
#            Question = models.get_model('questions', 'Question')
#            question = Question.objects.get(pk=self.question)
#            user = question.user
#            user.profile.reputation = user.profile.reputation + 5
#            user.save()


class Notification(models.Model):
    INVITED = 'I'
    FOLLOWED = 'F'
    NOTIFICATION_TYPES = [
        (INVITED, 'Invited'),
        (FOLLOWED, 'Followed'),
    ]

    _INVITED_TEMPLATE = u'<a href="/{0}/"><strong>{0}</strong></a> dared you to take the challenge:  <a href="{1}">{2}</a>'
    _FOLLOW_TEMPLATE = u'<a href="/{0}/"><strong>{0}</strong></a> is now following you'

    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    challenge = models.ForeignKey('challenges.Challenge', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.INVITED:
            return self._INVITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.challenge.get_absolute_url()),
                escape(self.challenge.title),
            )
        elif self.notification_type == self.FOLLOWED:
            return self._FOLLOW_TEMPLATE.format(
                escape(self.from_user.username),
            )
        else:
            return 'Something went wrong.'

    def get_summary(self, value):
        summary_size = 70
        value = mark_safe(value)
        value = strip_tags(value)
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])

        else:
            return value

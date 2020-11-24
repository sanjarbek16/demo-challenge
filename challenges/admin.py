from django.contrib import admin
from .models import Challenge, FinishChallenge, Joined
# Register your models here.
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title', 'task',)
    prepopulated_fields = {'slug': ('title',),}


class FinishChallengeAdmin(admin.ModelAdmin):
    list_display = ('score', 'video','challenge', 'profile')
    search_fields = ('score', 'profile',)

class JoinedAdmin(admin.ModelAdmin):
	list_display = ('challenge', 'profile')

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Joined, JoinedAdmin)
admin.site.register(FinishChallenge, FinishChallengeAdmin)

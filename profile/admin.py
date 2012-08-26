from django.contrib import admin

from profile.models import UserProfile, EmailNotification

class UserProfileAdmin(admin.ModelAdmin):
    # list_display = ()
    list_filter = ['user']

class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'dailyreminder', 'weeklysummary',)
    ordering = ('user',)
    list_filter = ['user']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailNotification, EmailNotificationAdmin)

from django.contrib import admin
from .models import DirectMessage


class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'date_of_message', 'time_of_message')


admin.site.register(DirectMessage, DirectMessageAdmin)

from django.contrib import admin
from .models import FriendRequest, FriendList


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')


class FriendListAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', )


admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(FriendList, FriendListAdmin)

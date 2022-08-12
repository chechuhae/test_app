from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)


class FriendList(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)
    date_of_friendship = models.DateTimeField('date_of_friendship', auto_now_add=True)

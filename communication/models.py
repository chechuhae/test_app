from django.db import models
from django.contrib.auth.models import User


class DirectMessage(models.Model):
    from_user = models.ForeignKey(User, related_name='mes_from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='mes_to_user', on_delete=models.CASCADE)
    # dialog_between = models.UniqueConstraint(fields=['from_user', 'to_user'], name='constraint_name')
    direct_message = models.CharField(max_length=1000)
    date_of_message = models.DateField(auto_now_add=True)
    time_of_message = models.TimeField(auto_now_add=True)

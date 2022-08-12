from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


User._meta.get_field('email')._unique = True


def user_directory_path(instance, filename):
    return 'images/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    town = models.CharField(max_length=25, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to=user_directory_path, default='default.png')

    def age(self):
        today = datetime.date.today()
        if self.date_of_birth:
            birthday = self.date_of_birth
        else:
            return "Input date of birth"
        return int((today - birthday).days // 365)

    age = property(age)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

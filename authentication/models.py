from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles", default="profiles/default.png")
    items_in_cart = models.IntegerField(default=0)




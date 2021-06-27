from collections import namedtuple
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _



class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
        
class Follow(models.Model):
    follower_user = models.ForeignKey(User, related_name="following", on_delete=CASCADE)

    following_user = models.ForeignKey(User, related_name="followers", on_delete=CASCADE)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower_user.username + " -> " + self.following_user.username


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='post', on_delete=CASCADE)
    context = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    like_count = models.DecimalField(max_digits=999999, decimal_places=0, default=0)
    tag = models.ManyToManyField(Tag, related_name='posts') 
    likes = models.ManyToManyField(User, related_name='likes', verbose_name=_("like post verbose field"))

    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.author.username + " : " + self.context



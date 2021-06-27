from .models import *
from django.contrib import admin

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','birth_date')

class FollowingAdmin(admin.ModelAdmin):
    list_display = ('follower_user','following_user')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author','context','created_date')



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowingAdmin)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Post, Comment, PostTag, CommentTag

admin.site.register(MyUser, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostTag)
admin.site.register(CommentTag)

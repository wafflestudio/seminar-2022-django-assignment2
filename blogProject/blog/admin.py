from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Tag)
admin.site.register(TagToPostOrComment)
admin.site.register(Post)
admin.site.register(Comment)

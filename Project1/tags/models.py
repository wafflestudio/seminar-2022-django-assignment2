from django.db import models

from comments.models import Comment
# Create your models here.

class Tag(models.Model):
    content = models.SlugField(max_length=20, primary_key=True)



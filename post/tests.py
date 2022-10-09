from django.test import TestCase
from django.contrib.auth.models import User

from .models import Post, Comment, Tag

# Create your tests here.


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a user
        testuser1 = User.objects.create_user(
            username="testuser1",
            password='password1'
        )
        testuser1.save()

        # create a blog post
        test_post = Post.objects.create(
            created_by=testuser1,
            title='Blog title',
            description='Body content ///',
            # tag
            # comment
        )
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        created_by = f'{post.created_by}'
        title = f'{post.title}'
        description = f'{post.description}'
        self.assertEqual(created_by, 'testuser1')
        self.assertEqual(title, 'Blog title')
        self.assertEqual(description, 'Body content ///')

## 낙서장
```python
>>> from post.models import Post, Comment, Tag
>>> from django.contrib.auth.models import User
>>> testuser = User.objects.create_user(username="testuser", password="password")
>>> p = Post.objects.create(title="Title", description="description", created_by=testuser)
>>> testtag = Tag.objects.create(name="tagname", content="content")
>>> p.tag.add(testtag)
>>> p.tag.all()
<QuerySet [<Tag: tagname>]>
```

```python
class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Book
        fields = ("id", "title", "description", "publisher", "release_date", "authors")
        extra_kwargs = {'authors': {'required': False}}
```
- Book 과 Author가 ManytoManyField
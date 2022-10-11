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

```json
{
	"username":"tomato",
	"password":"tomatohello"
}
```
```json
{
	"title":"title",
	"description":"description",
	"create_tag":"tag, tag, tag"
}
```
```json
{
	"title":"title",
	"description":"maintenance will be difficult and the OCP principle will be violatedOCP: (Open-Closed Principle)Software entities (classes, modules, functions, etc.) should be open for extension but closed for change.Problem solvingImplemented so that FactoryClass does not change even when services are added.maintenance will be difficult and the OCP principle will be violatedOCP: (Open-Closed Principle)Software entities (classes, modules, functions, etc.) should be open for extension but closed for change.Problem solvingImplemented so that FactoryClass does not change even when services are addedmaintenance will be difficult and the OCP principle will be violatedOCP: (Open-Closed Principle)Software entities (classes, modules, functions, etc.) should be open for extension but closed for change.Problem solvingImplemented so that FactoryClass does not change even when services are addedmaintenance will be difficult and the OCP principle will be violatedOCP: (Open-Closed Principle)Software entities (classes, modules, functions, etc.) should be open for extension but closed for change.Problem solvingImplemented so that FactoryClass does not change even when services are added",
	"create_tag":"tag, tag, tag"
}
```
https://github.com/nomadcoders/nomadgram/tree/master/nomadgram
노마드그램 참고하기 Django임
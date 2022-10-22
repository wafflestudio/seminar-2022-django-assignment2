# Test
- 성공/실패 : 예상 결과에 맞게 나오는지
- 에러 핸들링 : 예상치 못한 결과를 얼마나 잘 처리하는지
- 하나의 함수를 테스트
- test_forms.py, test_models.py, test_views.py
- django-webtest
- coverage
- django-discover-runner
- factory_boy, model_mommy
- https://realpython.com/testing-in-django-part-1-best-practices-and-examples/
- 마저 읽고 실행해보기

## User
- v1/user/register/
```json
{
	"username":"username1",
	"password":"password1",
	"nickname":"nickname1",
	"short_bio":"my name is youngzoo park",
	"url":"https://tomatolife.tistory.com/"
}
{
	"username":"username2",
	"password":"password2",
	"nickname":"nickname2",
	"short_bio":"my name is youngzoo park",
	"url":"https://tomatolife.tistory.com/"
}
```

- v1/user/login/
```json
{
	"username":"username",
	"password":"password"
}
```

- v1/user/follow/<str:username>/
- v1/user/unfollow/<str:username>/
- v1/user/profile/
  
## Post
- v1/post/
```json
{
	"title":"title",
	"description":"post content",
	"create_tag":"#post #django #backend #python"
}
```

- v1/post/<int:pk>/
- v1/post/<int:pk>/comment/
```json
{
	"content":"comment 남기고 갑니다",
	"parent_comment":1, 
	"create_tag":"#comment #tag #hashtag #create_tag"
}
```

- v1/post/<int:pk>/comment/<int:pk2>/
- v1/post/<int:pk>/clapse/
- v1/post/<int:pk>/unclapse/
- v1/post/tag/post/<str:tagname>
- v1/post/tag/comment/<str:tagname>/

## Notification
- v1/notification/

# 개선사항
- photo(ImageField)는 postman으로 어떻게 보내야하는지
  https://askcodes.net/coding/insomnia-upload-pic-and-post-data-at-same-time

# manytomanyfield serializer & view 구현 방법
- models
  - class Room
    - amenities = ..
  - class Amenity
    - name
    - description

- views
  - 

- 내 케이스
- models
  - class Post
    - tags
  - class Comment
    - tags
  - class Tag

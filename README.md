# Medium alternative : Large Scale Blog Service
![logo_new](https://user-images.githubusercontent.com/81140673/196366827-142b7ced-6cf0-426b-b72c-a1f7b68e7b60.png)
- 작성자 : 박용주 (2022.10.24)


<br></br>

# Table of content
- [Medium alternative : Large Scale Blog Service](#medium-alternative--large-scale-blog-service)
- [Table of content](#table-of-content)
- [Overview](#overview)
  - [User API Example](#user-api-example)
  - [Post API example](#post-api-example)
- [Notification App](#notification-app)
  - [Models](#models)
  - [Urls](#urls)
  - [Views](#views)
  - [environment](#environment)
<br></br>

# Overview
![new명세](https://user-images.githubusercontent.com/81140673/200158751-3a95ea8e-97ad-48fa-85c7-0045455749ef.png)

- Medium alternative은 User, Post, Notification 앱으로 구성된 장고 프로젝트입니다. 


- User 앱에는 회원가입, 로그인, 마이페이지 기능, 


- Post 앱에는 Post, Comment(대댓글), Clapse, Clapse, Tag 기능이 있으며, 


- Notification 앱에는 알림 기능을 구현하였습니다. 


<br></br>

## User API Example
- POST /v1/user/register/
```json
{
  "username":"username", //required
  "password":"password", //required
  "nickname":"nickname",
  "short_bio":"short_bio",
  "url":"https://tomatolife.tistory.com/"
  // photo : insomnia setting에서 전송
}
```
- POST /v1/user/login/
```json
{
  "username":"username",
  "password":"password"
}
```

- POST /v1/user/follow/<str:username>/
```json
no content
```

- POST /v1/user/unfollow/<str:username>/
```json
no content
```

- GET /v1/user/profile/


<br></br>

## Post API example
- GET /v1/post/


- POST /v1/post/
```json
{
  "title":"title",
  "description":"description",
  "create_tag":"#tag #comment #python" //선택
}
```

- GET /v1/post/<int:pk>/
- PUT /v1/post/<int:pk>/
```json
{
  "title":"title",
  "description":"description",
  "create_tag":"#tag #comment #python" //선택
}
```

- DELETE /v1/post/<int:pk>/
- GET /v1/post/<int:pk>/comment/
- POST /v1/post/<int:pk>/comment/
```json
{
  "content":"content",
  "parent_comment":1, // 선택
  "create_tag":"#tag #comment #python" //선택
}
```

- PUT /v1/post/<int:pk>/comment/<int:pk2>/
```json
{
  "content":"content",
  "parent_comment":1, // 선택
  "create_tag":"#tag #comment #python" //선택
}
```

- DELETE /v1/post/<int:pk>/comment/<int:pk2>/
- GET /v1/post/<int:pk>/clapse/
- POST /v1/post/<int:pk>/clapse/
- DELETE /v1/post/<int:pk>/unclapse/
- GET /v1/post/tag/<str:tagname>/post/
- GET /v1/post/tag/<str:tagname>/comment/

# Notification App
- Notification 앱은 사용자에게 알림을 보내는 기능을 합니다. 
<br></br>

## Models
- Notification 모델은 다음과 같습니다. 

|Field|Type|
|-|-|
|notify_from|ForeignKey(User)|
|notify_to|ForeignKey(User)|
|notification_type|CharField|
|post|ForeignKey(Post)|
|comment|TextField|
|created_at|DateTimeField|

<br></br>

## Urls
- Notification URL은 다음과 같습니다. 


|url|viewset|authentication|
|-|-|-|
|''|NotificationList|O|

<br></br>

## Views
- Notification View는 다음과 같습니다. 


|Class|Method|Authentication|
|-|-|-|
|NotificationList|Get|O|

<br></br>

## environment
- Windows wsl
- [requirements.txt](/requirements.txt)

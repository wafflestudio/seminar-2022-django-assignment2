# Medium alternative : Large Scale Blog Service
![logo_new](https://user-images.githubusercontent.com/81140673/196366827-142b7ced-6cf0-426b-b72c-a1f7b68e7b60.png)
- 작성자 : 박용주 (2022.10.24)


<br></br>

# Table of content
- [Medium alternative : Large Scale Blog Service](#medium-alternative--large-scale-blog-service)
- [Table of content](#table-of-content)
- [Overview](#overview)
- [User App](#user-app)
  - [Models](#models)
  - [Urls](#urls)
  - [Views](#views)
- [Post App](#post-app)
  - [Models](#models-1)
    - [Post model](#post-model)
    - [Comment model](#comment-model)
    - [Clapse model](#clapse-model)
    - [Tag model](#tag-model)
  - [Urls](#urls-1)
  - [Views](#views-1)
- [Notification App](#notification-app)
  - [Models](#models-2)
  - [Urls](#urls-2)
  - [Views](#views-2)
  - [environment](#environment)
<br></br>

# Overview
![new명세](https://user-images.githubusercontent.com/81140673/196373512-fc2c68a4-f84e-4c1c-aa44-d33604727ec6.png)
- Medium alternative은 User, Post, Notification 앱으로 구성된 장고 프로젝트입니다. 


- User 앱에는 회원가입, 로그인, 마이페이지 기능, 


- Post 앱에는 Post, Comment(대댓글), Clapse, Clapse, Tag 기능이 있으며, 


- Notification 앱에는 알림 기능을 구현하였습니다. 


<br></br>

# User App
- User 앱은 로그인, 회원가입, 프로파일 등 User 관련 기능을 관리합니다. 

## Models
- User model은 다음과 같습니다. 
  
|Fields|Type|
|-|-|
|username|CharField|
|password|CharField|
|nickname|CharField|
|short_bio|CharField|
|photo|ImageField|
|url|URLField|
|followers|ManyToManyField('self')|
|following|ManyToManyField('self')|
|post_count|self.post.all().count()|
|followers_count|self.followers.all().count()|
|following_count|self.following.all().count()|
<br></br>

## Urls
- User 앱의 url 설계는 다음과 같습니다. 


|기능|url|viewset|Authentication|
|-|-|-|-|
|회원가입|register/|Register| - |
|로그인|login/|Login|-|
|팔로우|<int:pk>/follow/|FollowUser|O|
|언팔로우|<int:pk>/unfollow/|UnFollowUser|O|
|마이페이지|profile/|UserProfile|O|

<br></br>

## Views
- User 앱의 view는 다음과 같습니다. 

|class|method|기능|Authentication|
|-|-|-|-|
|RegisterUser|Post|회원가입|X|
|LoginView|Post|로그인|X|
|FollowUser|Post|팔로우|O|
|UnFollowUser|Delete|언팔로우|O|
|UserProfile|Get|마이페이지|O|

<br></br>

# Post App
- Post 앱은 Post, Comment, Clapse, Tag 기능을 담당합니다. 
  - Post : 블로그 포스트 CRUD
  - Comment : 댓글 CRUD
  - Clapse : Medium alternative의 좋아요 기능을 합니다
  - Tag : Post와 Comment의 Hash Tag를 저장합니다

<br></br>

## Models
### Post model
- Post 앱의 Post model은 다음과 같습니다. 


|Field|Type|
|-|-|
|created_by|ForeignKey(User)|
|created_at|DateTimeField|
|updated_at|DateTimeField|
|title|CharField|
|description|TextField|
|summary_for_listing|CharField|
|n_min_read|IntegerField|
|create_tag|CharField|
|tag|ManyToManyField('Tag')|
|clapse_count|self.clapse.all().count()|
|comment_count|self.comment.all().count()|

### Comment model
- Post 앱의 Comment model은 다음과 같습니다. 


|Field|Type|
|-|-|
|post|ForeignKey(Post)|
|created_by|ForeignKey(User)|
|created_at|DateTimeField|
|updated_at|DateTimeField|
|is_updated|BooleanField|
|content|TextField|
|parent_comment|ForeignKey('self')|
|create_tag|CharField|
|tag|ManyToManyField('Tag')|


### Clapse model
- Post 앱의 Clapse model은 다음과 같습니다. 


|Field|Type|
|-|-|
|post|ForeignKey(Post)|
|created_by|ForeignKey(User)|
|created_at|DateTimeField|



### Tag model
- Post 앱의 Tag model은 다음과 같습니다. 


|Field|Type|
|-|-|
|name|CharField|
|created_at|DateTimeField|
|content|CharField|

<br></br>

## Urls
- Post 앱의 URL은 다음과 같습니다. 



|url|viewset|authentication|
|-|-|-|
|''|PostList|O|
|<int:pk>/|PostDetail|O|
|<int:pk>/comment/|CommentList|O|
|<int:pk>/comment/<int:pk2>/|CommentDetail|O|
|<int:pk>/clapse/|ClapseList|O|
|<int:pk>/unclapse/|UnClapseList|O|
|tag/post/|TagPostList|X|
|tag/comment/|TagCommentList|X|

<br></br>

## Views
- Post 앱의 View는 다음과 같습니다. 


|Class|Method|Authentication|
|-|-|-|
|PostList|Get|X|
| |Post|O|
|PostDetail|Get|X|
| |Put|O|
| |Delete|O|
|CommentList|Get|X|
| |Post|O|
|CommentDetail|Put|O|
| |Delete|O|
|ClapseList|Get|X|
| |Post|O|
|UnClapseList|Delete|O|
|TagPostList|Get|X|
|TagCommentList|Get|X|

<br></br>

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

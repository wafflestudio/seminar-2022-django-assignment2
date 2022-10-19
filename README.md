# Medium alternative : Large Scale Blog Service
![logo_new](https://user-images.githubusercontent.com/81140673/196366827-142b7ced-6cf0-426b-b72c-a1f7b68e7b60.png)
- 작성자 : 박용주 (2022.10.13)


<br></br>

# Overview
![new명세](https://user-images.githubusercontent.com/81140673/196373512-fc2c68a4-f84e-4c1c-aa44-d33604727ec6.png)

<br></br>

# User App
## Models
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
|기능|url|viewset|Authentication|
|-|-|-|-|
|회원가입|register/|Register| - |
|로그인|login/|Login|-|
|팔로우|<int:pk>/follow/|FollowUser|O|
|언팔로우|<int:pk>/unfollow/|UnFollowUser|O|
|마이페이지|profile/|UserProfile|O|

<br></br>

## Views
|class|method|기능|Authentication|
|-|-|-|-|
|RegisterUser|Post|회원가입|X|
|LoginView|Post|로그인|X|
|FollowUser|Post|팔로우|O|
|UnFollowUser|Delete|언팔로우|O|
|UserProfile|Get|마이페이지|O|

<br></br>

# Post App
<br></br>

## Models
### Post model
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
|Field|Type|
|-|-|
|post|ForeignKey(Post)|
|created_by|ForeignKey(User)|
|created_at|DateTimeField|



### Tag model
|Field|Type|
|-|-|
|name|CharField|
|created_at|DateTimeField|
|content|CharField|

<br></br>

## Urls
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
|Class|Method|Authentication|
|-|-|-|
|PostList|Get|X|
||Post|O|
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
<br></br>

## Models
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
|url|viewset|authentication|
|-|-|-|
|''|NotificationList|O|

<br></br>

## Views
|Class|Method|Authentication|
|-|-|-|
|NotificationList|Get|O|

<br></br>

## environment
<<<<<<< HEAD
- Windows wsl
- requirements.txt
=======
- requirements.txt
>>>>>>> main

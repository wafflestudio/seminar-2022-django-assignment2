# Assignment 2 구현 설명

/medium/posts
Post create, list

/medium/posts/<int:pk>
Post detail, update, delete

/medium/posts/<int:pk>/comments
Post의 comments list

/medium/posts/tags/<str:content>
content의 Tag를 가진 Post list

/medium/comments/
Comment create, list

/medium/commnets/<int:pk>
Comment update, delete

/medium/comments/tags/<str:content>
content의 Tag를 가진 Comment list

/medium/register
User create : id, password, email로 User 생성
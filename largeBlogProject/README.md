### user
```
POST /users/register/ create a user
POST /users/login/ obtain a token by username and password
```

### post
```
GET /posts/ list posts
POST /posts/ create a post

GET /posts/:id detail a post
PUT /posts/:id update a post
PATCH /posts/:id partial update a post
DELETE /posts/:id delete a post
```

GET /posts/

| Arguments | 설명                         |
|-----------|----------------------------|
| tag       | 해당 태그가 달린 post list를 불러온다. |

### comment
```
GET /comments/ list comments
POST /comments/ create a comment

PUT /comments/:id update a comment
PATCH /comments/:id partial update a comment
DELETE /comments/:id delete a comment
```

GET /comments/

| Arguments | 설명                              |
|-----------|---------------------------------|
| post      | 해당 post에 달린 comment list를 불러온다. |
| tag       | 해당 태그가 달린 comment list를 불러온다.   |
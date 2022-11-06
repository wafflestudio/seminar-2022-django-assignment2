# Large Blog REST API Reference

## Follower-Following System

### List the user's followings

`GET /users/:id/following/`

### List the user's followers

`GET /users/:id/followers/`

### Follow a user

`POST /users/:id/following/`

| Argument       | Type    | Detail      |
|----------------|---------|-------------|
| following_user | integer | 팔로우할 유저의 id |

### Unfollow a user

`DELETE /users/:id/following/:following_id/`

## Post

### Model

| Field        | Type     | Detail                |
|--------------|----------|-----------------------|
| id           | integer  | 고유 식별자.<br/>읽기 전용     |
| created_by   | integer  | 작성한 유저의 id.<br/>읽기 전용 |
| created_at   | datetime | 최초 작성 시각.<br/>읽기 전용   |
| updated_at   | datetime | 마지막 수정 시각.<br/>읽기 전용  |
| title        | string   | 글의 제목                 |
| reading_time | integer  | 읽는 시간                 |
| tags         | array    | 태그                    |
| description  | string   | 글의 본문                 |


### List posts

`GET /posts/`

| Argument | Detail                    |
|----------|---------------------------|
| tag      | 결과를 해당 태그가 달린 post로 한정한다. |

### Create a post

`POST /posts/`

| Argument     | Detail                                     |
|--------------|--------------------------------------------|
| tag          | 여러 태그를 등록할 수 있다.<br/>예시: `c, java, python` |
| title        | 필수                                         |
| reading_time |                                            |
| description  | 필수                                         |

### Retrieve a post

`GET /posts/:id`

### Update a post

`PUT /posts/:id` update a post

`PATCH /posts/:id` partial update a post

Arguments는 글을 생성할 때와 동일하다.

### Delete a post

`DELETE /posts/:id`

## Comment

### Model

| Field      | Type     | Detail                   |
|------------|----------|--------------------------|
| id         | integer  | 고유 식별자.<br/>읽기 전용        |
| post       | integer  | 원글의 id.<br/>읽기 전용        |
| created_by | integer  | 작성한 유저의 id.<br/>읽기 전용    |
| created_at | datetime | 최초 작성 시각.<br/>읽기 전용      |
| updated_at | datetime | 마지막 수정 시각.<br/>읽기 전용     |
| is_updated | boolean  | 최초 작성 후 수정 여부.<br/>읽기 전용 |
| tags       | array    | 태그                       |
| content    | string   | 댓글의 본문                   |


### List comments

`GET /comments/`

| Argument | Detail                         |
|----------|--------------------------------|
| post     | 결과를 해당 post에 달린 comment로 한정한다. |
| tag      | 결과를 해당 태그가 달린 comment로 한정한다.   |

### Create a comment

`POST /comments/`

| Argument    | Detail                                 |
|-------------|----------------------------------------|
| tag         | 여러 태그를 등록할 수 있다. 예시: `c, java, python` |
| content     | 필수                                     |
| post        | 필수                                     |

### Retrieve a comment

`GET /comments/:id`

### Update a comment

`PUT /comments/:id` update a comment

`PATCH /comments/:id` partial update a comment

Arguments는 댓글을 생성할 때와 동일하다.

### Delete a comment

`DELETE /comments/:id`

## User

### Sign Up

`POST /users/signup/`

| Argument         | Required |
|------------------|----------|
| Username         | true     |
| Password         | true     |
| Password confirm | true     |
| Email            | true     |
| First name       | false    |
| Last name        | false    |

### Sign In

`POST /users/signin/`

| Argument         | Required |
|------------------|----------|
| Username         | true     |
| Password         | true     |

| Return Value |
|--------------|
| Auth Token   |
# Medium Blog API
[![Python 3.8.11](https://img.shields.io/badge/python-3.8.11-blue.svg)](https://www.python.org/downloads/release/python-3811/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
#

## Prerequisite

To make python virtual env, follow below script

```bash
$ pyenv virtualenv 3.8.11 medium
$ pyenv activate medium
$ pip install -r requirements.txt
```

We use docker for using postgres db, but you can also use local postgres.
You have to change `username` and `password` in [settings.py](https://github.com/fivessun5/seminar-2022-django-assignment2/blob/da25f010cf99cc12c5455229d2270d7806c39953/medium/medium/settings.py).



#

## Deploy Cycle

### Convention
- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [black](https://black.readthedocs.io/en/stable/)
- [isort](https://pycqa.github.io/isort/)


Before add & commit to branch. 
```bash
$ sh reformat.sh # -> black, isort
```

# 
## API Summary

- user/ : sign-up

- blog/ : post, comment, tag


| methods                         | url                                          | description                               |
|---------------------------------|----------------------------------------------|-------------------------------------------|
| `POST`                          | `user/signup/`                               | sign-up user                              |
| `GET`                           | `user/login/`                                | login user : get token                    |
| `GET`, `POST`                   | `blog/post/`                                 | create post or get post list              |
| `GET`, `PUT`, `PATCH`, `DELETE` | `blog/post/\<int:pid\>/`                     | handle specific post                      |
| `GET`, `POST`                   | `blog/post/\<int:pid\>/comment/`             | create or get comment for specific post   |
| `PUT`, `PATCH`, `DELETE`        | `blog/post/\<int:pid\>/comment/\<int:cid\>/` | handle specific comment                   |
| `GET`                           | `blog/tag/post`                              | get all posts which contains tag          |
| `GET`                           | `blog/tag/comment`                           | get all comments which contains tag       |

#

## API Call & Response Example

### Sign up

```bash
# API Call
curl --request POST \
  --url http://127.0.0.1:8000/user/signup/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "user1",
	"password": "password1@",
	"password2": "password1@",
	"email": "user1@example.com",
	"first_name": "user1",
	"last_name": "user1"
}'

```

```json
# Response
{
	"username": "user1",
	"email": "user1@example.com",
	"first_name": "user1",
	"last_name": "user1"
}
```

### Login

```bash
# API Call
curl --request POST \
  --url http://127.0.0.1:8000/user/login/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "user1",
	"password": "password1@",
	"password2": "password1@",
	"email": "user1@example.com",
	"first_name": "user1",
	"last_name": "user1"
}'
```

```json
# Response
{
	"Token": "905XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

### Post New Blog Post

```bash
# API Call
curl --request POST \
  --url http://127.0.0.1:8000/user/login/ \
  --header 'Authorization: Token 905XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "user1",
	"password": "password1@",
	"password2": "password1@",
	"email": "user1@example.com",
	"first_name": "user1",
	"last_name": "user1"
}'
```

### Get All Blog Post Which contains all input tags

```bash
# API Call
curl --request GET \
  --url http://127.0.0.1:8000/blog/tag/post/ \
  --header 'Content-Type: application/json' \
  --data '{
	"tags": [
		{
			"name": "tag1"
		}, 
		{
			"name": "tag2"
		}
	],
	"option": "and"
}'
```

```json
# Response
[
	{
		"pid": 2,
		"tags": [
			{
				"name": "tag1"
			},
			{
				"name": "tag2"
			}
		],
		"title": "test post 2 : title",
		"created_at": "2022-11-12T15:03:24.631312Z",
		"updated_at": "2022-11-12T15:03:24.631336Z",
		"content": "test post 2 : content",
		"url": "",
		"created_by": 1
	},
	{
		"pid": 3,
		"tags": [
			{
				"name": "tag1"
			},
			{
				"name": "tag2"
			},
			{
				"name": "tag3"
			}
		],
		"title": "test post 3 : title",
		"created_at": "2022-11-12T15:03:35.814587Z",
		"updated_at": "2022-11-12T15:03:35.814610Z",
		"content": "test post 3 : content",
		"url": "",
		"created_by": 1
	}
]
```


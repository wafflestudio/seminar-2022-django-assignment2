# Medium Blog API

## App Docs

- user : sign-up

- blog : post, comment, tag


| methods                         | url                                          | description                               |
|---------------------------------|----------------------------------------------|-------------------------------------------|
| `POST`                          | `user/register/`                             | sign-up user                              |
| `GET`, `POST`                   | `blog/post/`                                 | create post or get post list              |
| `GET`, `PUT`, `PATCH`, `DELETE` | `blog/post/\<int:pid\>/`                     | handle specific post                      |
| `GET`, `POST`                   | `blog/post/\<int:pid\>/comment/`             | create or get comment for specific post   |
| `PUT`, `PATCH`, `DELETE`        | `blog/post/\<int:pid\>/comment/\<int:cid\>/` | handle specific comment                   |

#

## Prerequisite

```bash
$ pyenv virtualenv 3.8.11 medium
$ pyenv activate medium
$ pip install -r requirements.txt
```

#

## Deploy Cycle

Before push to git branch. 
```bash
$ sh reformat.sh # -> black, isort
```

